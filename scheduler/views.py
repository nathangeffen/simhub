"""
Views for gambling simulation
"""

import os
import ntpath
import sys
import subprocess
import json
import threading
import logging
from enum import Enum

from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.translation import gettext as _

from .exceptions import QueueFull
from . import settings

logger = logging.getLogger("scheduler")


class DictActions(Enum):
    GET = 1
    DEL = 2
    REMOVE = 3


class JobView:
    """Handles queueing and running of simulation jobs submitted via a html form.
    """

    # Private
    key_prefix = ""
    _open_files_lock = threading.Lock()
    _open_files = {}

    _proc_lock = threading.Lock()
    _running = []
    _waiting = []
    _job_queue = {}
    _env = os.environ.copy()

    def _open_files_action(self, key, action=DictActions.GET):
        filename = self._get_output_filename(key)
        result = None
        with self._open_files_lock:
            if action == DictActions.GET:
                if filename in self._open_files:
                    result = self._open_files[filename]
                else:
                    try:
                        f = open(filename, "r")
                        self._open_files[filename] = f
                        result = f
                    except FileNotFoundError:
                        result = None
            elif action == DictActions.DEL:
                try:
                    if filename in self._open_files:
                        f = self._open_files[filename]
                        f.close()
                        del self._open_files[filename]
                except (IOError, KeyError) as e:
                    logger.error(e)
            elif action == DictActions.REMOVE:
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
                except IOError as e:
                    logger.error(e)
        return result

    def _put_job_in_queue(self, job):
        key = job["key"]
        with self._proc_lock:
            if len(self._waiting) >= settings.MAX_JOBS_WAITING:
                raise QueueFull
            self._waiting.insert(0, key)
            self._job_queue[key] = {}
            self._job_queue[key]["command"] = job["command"]
            self._job_queue[key]["finished"] = False
            self._job_queue[key]["timeout"] = False
            self._job_queue[key]["timeout_time"] = timezone.now()
            self._job_queue[key]["fail"] = None
            self.set_ping_time(key)
        self._run_job_from_queue()

    def _execute(self, key, command):
        timeout = False
        fail = None
        try:
            result = self.run(command, key)
            if result.returncode is not 0:
                head, tail = ntpath.split(command[0])
                fail = f"{tail} returned error code {result.returncode}."
        except subprocess.TimeoutExpired:
            timeout = True
        except Exception as e:
            print(e)
            fail = e.__doc__
            logger.error(fail)
        with self._proc_lock:
            self._job_queue[key]["finished"] = True
            self._job_queue[key]["timeout"] = timeout
            self._job_queue[key]["fail"] = fail
            if key in self._running:
                self._running.remove(key)
            is_waiting = len(self._waiting)
        if is_waiting:
            self._run_job_from_queue()

    def _run_job_from_queue(self):
        with self._proc_lock:
            if len(self._running) >= settings.MAX_JOBS_RUNNING:
                pass
            elif len(self._waiting) > 0:
                key = self._waiting.pop()
                self._running.append(key)
                command = self._job_queue[key]["command"]
                self._job_queue[key]["process"] = \
                                    threading.Thread(target=self._execute,
                                                     args=(key, command, ))
                self._job_queue[key]["process"].start()

    def _read_output_file(self, key, currentpos, numlines):
        proc_file = self._open_files_action(key, DictActions.GET)
        extra_chars = 0
        if proc_file:
            proc_file.seek(currentpos)
            lines = []
            for _ in range(numlines):
                line = proc_file.readline()
                if line:
                    if line[-1] == '\n':
                        lines.append(line)
                    else:
                        extra_chars = len(line)
                        break
                else:
                    break
            return lines, proc_file.tell() - extra_chars
        else:
            return [], 0

    def _process_not_running(self, key):
        try:
            with self._proc_lock:
                index = self._waiting.index(key)
            msg = _(f"Your job is number {index + 1} in the queue")
        except ValueError:
            msg = _("Starting ...")
        return msg

    def _get_output_filename(self, key):
        filename = settings.OUTPUT_FILE_PREFIX + key + \
                   settings.OUTPUT_FILE_SUFFIX
        full_filename = os.path.join(settings.OUTPUT_FILE_DIR, filename)
        return full_filename

    # Public methods

    def run(self, command, key=None):
        try:
            prog_out = subprocess.run(command, timeout=settings.TIMEOUT,
                                      env=self._env,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            if prog_out.returncode > 0:
                raise RuntimeError("Return code > 0")
        except (RuntimeError, subprocess.CalledProcessError) as e:
            logger.error(f"{e}. Check file {self._get_output_filename(key)}")
            with open(self._get_output_filename(key), 'w') as f:
                f.write(prog_out.stderr.decode("utf-8"))
        return prog_out

    def set_ping_time(self, key):
        self._job_queue[key]["ping"] = timezone.now()

    def remove_zombies(self):
        '''Removes entries from _job_queue that have been left hanging around.  This is
        potentially a time-consuming process that uses _proc_lock. The main
        logic is therefore only executed when _job_queue has a large number of
        entries.
        '''
        with self._proc_lock:
            if len(self._job_queue) > settings.ZOMBIE_REMOVAL_QUEUE_SIZE:
                key_dict = []
                for key in self._job_queue:
                    key_dict.append(key)
                for key in key_dict:
                    if self._job_queue[key]["finished"] is True:
                        diff = timezone.now() - self._job_queue[key]["ping"]
                        if diff.seconds > settings.NO_PING_TIMEOUT:
                            self._remove_job_no_lock(key)

    def is_timeout(self, key):
        '''Besides checking if a job has timed out, this function has the important side
        effect of calling the remove zombie method. Doesn't seem a better place
        to put it.
        '''
        with self._proc_lock:
            timeout = self._job_queue[key]["timeout"]
        self.remove_zombies()
        return timeout

    def is_fail(self, key):
        with self._proc_lock:
            fail = self._job_queue[key]["fail"]
        return fail

    def set_env(self, key, val):
        self._env[key] = val

    def job_in_queue(self, key):
        result = False
        with self._proc_lock:
            if key in self._running or key in self._waiting:
                result = True
        return result

    def job_exists(self, key):
        result = False
        with self._proc_lock:
            if key in self._job_queue:
                result = True
        return result

    def _remove_job_no_lock(self, key):
        if key in self._running:
            self._running.remove(key)
        if key in self._waiting:
            self._waiting.remove(key)
        if key in self._job_queue:
            del self._job_queue[key]

    def remove_job(self, key):
        with self._proc_lock:
            self._remove_job_no_lock(key)

    def print_queues(self, verbose=True):
        ''''Prints the list of jobs running, those that are waiting, and then a
        dictionary of all jobs and their corresponding data.
        '''
        print(f"Running: {self._running}. Waiting {self._waiting}.")
        if verbose:
            print(self._job_queue)

    def context_data_get(self, request, form_cls):
        request.session["errormsg"] = ""
        request.msgstatus = "info"
        duplicate = 0
        if "key" not in request.session:
            request.session.cycle_key()
            request.session["key"] = self.key_prefix + \
                request.session.session_key
        form = form_cls()
        if "status" not in request.session or \
           self.job_exists(request.session["key"]) is False or \
           self.job_in_queue(request.session["key"]) is False or \
           self.is_timeout(request.session["key"]) or \
           self.is_fail(request.session["key"] is not None):
            request.session["status"] = "idle"
        data = {
            'form': form,
            'duplicate': duplicate,
            'key': request.session["key"]
        }
        return data

    def context_data_post(self, request, form_cls, view_cls):
        request.session["errormsg"] = ""
        request.msgstatus = "running"
        duplicate = 0

        form = form_cls(request.POST, request.FILES)
        if form.is_valid():
            if request.session["status"] == "idle":
                key = request.session["key"]
                job = {}
                job["key"] = key
                job["command"] = view_cls.command_line(form.cleaned_data,
                                                       request.FILES,
                                                       key)
                try:
                    self._open_files_action(key, DictActions.REMOVE)
                    self._put_job_in_queue(job)
                    request.session["status"] = "running"
                except QueueFull:
                    request.session["status"] = "idle"
                    request.session["errormsg"] = _("Too many jobs running. "
                                                    "Please try later.")
                request.session["linesProcessed"] = 0
                request.session["filePos"] = 0
        else:
            messages.add_message(request, messages.ERROR,
                                 "Please fix the errors")
        data = {
            'form': form,
            'duplicate': duplicate,
            'key': request.session["key"]
        }
        return data

    def context_data(self, request, context=None, form_cls=None,
                     view_cls=None):
        data = {}
        if request.method == 'GET':
            data = self.context_data_get(request, form_cls)
        elif request.method == 'POST':
            data = self.context_data_post(request, form_cls, view_cls)
        context['form'] = data['form']
        context['duplicate'] = data['duplicate']
        context['key'] = data['key']
        return context


class JobFormView(JobView, FormView):
    form_class = None

    def get_output_filename(self):
        return self._get_output_filename(self.request.session["key"])

    def command_line(self, data=None, files=None, key=None):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.context_data(request=self.request, context=context,
                                    form_cls=self.form_class, view_cls=self)
        return context

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class JobJSONView(TemplateView):
    job_view_cls = JobFormView()
    context_keys = ("lines", "msg", "msgstatus", )
    lines_to_read = settings.LINES_TO_READ

    def _get_data_running(self, context, key):
        is_finished = False
        fail = self.job_view_cls.is_fail(key)
        if self.job_view_cls.is_timeout(key):
            self.request.session["status"] = context["status"] = "idle"
            context['msg'] = _("Sorry, job took too much time. ")
            context['msgstatus'] = "error"
        elif fail is not None:
            logger.warning(f"Job for key {key} failed with code {fail}")
            self.request.session["status"] = context["status"] = "idle"
            context['msg'] = _("Sorry, job failed.")
            context['msgstatus'] = "error"

        with self.job_view_cls._proc_lock:
            is_running = (key in self.job_view_cls._running)
            is_finished = self.job_view_cls._job_queue[key]["finished"]
        if is_running or is_finished:
            prev_pos = self.request.session["filePos"]
            context['lines'], self.request.session["filePos"] = \
                self.job_view_cls._read_output_file(
                    key, self.request.session["filePos"],
                    self.lines_to_read)
        else:
            self.request.session["filePos"] = prev_pos = 0

        if (fail is None) and \
           (self.job_view_cls.is_timeout(key) is False):
            if is_finished and (prev_pos == self.request.session["filePos"]):
                self.request.session["status"] = "idle"
                self.request.session["filePos"] = 0
                context['msg'] = _("Your job finished successfully.")
                context['msgstatus'] = "success"
                self.request.session["status"] = context["status"] = "idle"
                self.job_view_cls._open_files_action(key, DictActions.DEL)
                self.job_view_cls.remove_job(key)
            elif self.request.session["filePos"] == 0:
                context['msg'] = self.job_view_cls._process_not_running(key)
                context['msgstatus'] = "info"
            else:
                self.request.session["status"] = "running"
                context['msg'] = _("Running ...")
        return context

    def post_process(self, dict):
        return dict

    def get_data(self, context):
        """Sets the asynchronously obtained lines, msg and msgstatus
        entries in the context, which must subsequently be returned in
        JSON format. As a side effect, also sets the session status back
        to idle if the job is finished or there's an error.
        """
        dict = {}
        for key in self.context_keys:
            if key in context:
                dict[key] = context[key]

        dict['lines'] = []
        dict['msgstatus'] = "info"
        dict["msg"] = ""
        key = self.request.session["key"]
        self.job_view_cls.set_ping_time(key)
        try:
            if self.request.session["status"] == "running" and \
               self.job_view_cls.job_exists(key):
                context = self._get_data_running(dict, key)
            else:
                self.request.session["status"] = "idle"
        except IOError as e:
            logger.error(e)
            self.request.session["status"] = "idle"
            dict['msg'] = _("Sorry, there was a problem on the server.")
            dict['msgstatus'] = "error"
        return self.post_process(dict)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)
