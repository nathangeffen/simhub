"""
Views for faststi simulation
"""

import os
import subprocess
import logging
from pathlib import Path

from django.http import HttpResponse
from django.http import Http404

from scheduler.views import JobFormView
from scheduler.settings import OUTPUT_FILE_DIR, TIMEOUT
from .settings import DATA_DIR, EXE_DIR, EXE_NAME
from .forms import FaststiForm

logger = logging.getLogger("faststi")

def handle_uploaded_file(f, filename):
    with open(filename, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class FaststiFormView(JobFormView):
    template_name = 'faststi/faststi_form.html'
    form_class = FaststiForm

    def __init__(self):
        super(FaststiFormView, self).__init__()
        self.set_env("FSTI_DATA", DATA_DIR)

    def _write_initial_gen(self, f, fields):
        f.write("sex;sex_preferred;age|5-YEAR;1;2;3;4|4\n")
        f.write("0;0;0;0.0;0.0;0.0;0.0\n")
        f.write("0;0;1;0.0;0.0;0.0;0.0\n")
        f.write("0;0;2;0.0;0.0;0.0;0.0\n")
        j = 3
        for i in range(7):
            f.write(
                f"0;0;{j};{fields[i][1]};{fields[i][2]};"
                f"{fields[i][3]};{fields[i][4]}\n")
            j = j + 1
        f.write("0;1;0;0.0;0.0;0.0;0.0\n")
        f.write("0;1;1;0.0;0.0;0.0;0.0\n")
        f.write("0;1;2;0.0;0.0;0.0;0.0\n")
        j = 3
        for i in range(7,14):
            f.write(
                f"0;1;{j};{fields[i][1]};{fields[i][2]};"
                f"{fields[i][3]};{fields[i][4]}\n")
            j = j + 1
        f.write("1;0;0;0.0;0.0;0.0;0.0\n")
        f.write("1;0;1;0.0;0.0;0.0;0.0\n")
        f.write("1;0;2;0.0;0.0;0.0;0.0\n")
        j = 3
        for i in range(14,21):
            f.write(
                f"1;0;{j};{fields[i][1]};{fields[i][2]};"
                f"{fields[i][3]};{fields[i][4]}\n")
            j = j + 1
        f.write("1;1;0;0.0;0.0;0.0;0.0\n")
        f.write("1;1;1;0.0;0.0;0.0;0.0\n")
        f.write("1;1;2;0.0;0.0;0.0;0.0\n")
        j = 3
        for i in range(21,28):
            f.write(
                f"1;1;{j};{fields[i][1]};{fields[i][2]};"
                f"{fields[i][3]};{fields[i][4]}\n")
            j = j + 1

    def _write_mortality(self, f, fields):
        f.write("infected;age|5-YEAR;sex;prob\n")
        for i in range(5):
            f.write(f"{i};0;0;0.0\n"
                    f"{i};0;1;0.0\n"
                    f"{i};1;0;0.0\n"
                    f"{i};1;1;0.0\n"
                    f"{i};2;0;0.0\n"
                    f"{i};2;1;0.0\n")
            for j in range(3,10):
                for k in range(0,2):
                    f.write(f"{i};{j};{k};{fields[(j-3)*(k+1)][i]}\n")

    def _write_infect(self, f, fields):
        f.write("sex;sex|1|~;infected;0\n")
        l = 0
        for i in range(2):
            for j in range(2):
                for k in range(5):
                    f.write(f"{i};{j};{k};{fields[i*2+j][k]}\n")

    def _write_boiler_plate_config(self, f, key):
        f.write(
            "dataset_gen_sex=dataset_gen_sex.csv\n"
            "dataset_gen_sex_preferred=dataset_gen_sex_preferred.csv\n"
            "dataset_gen_treated=dataset_gen_treated.csv\n"
            "dataset_gen_resistant=dataset_gen_resistant.csv\n"
            "dataset_gen_mating=dataset_gen_mating.csv\n"
            "dataset_birth_infect=dataset_gen_infect.csv\n"
            "dataset_birth_treated=dataset_birth_treated.csv\n"
            "dataset_birth_resistant=dataset_birth_resistant.csv\n"
            "dataset_rel_period=dataset_rel.csv\n"
            "dataset_single_period=dataset_single.csv\n"
            "dataset_infect_stage=dataset_infect_stage.csv\n"
            "before_events=_write_results_csv_header;"
            "_generate_and_pair\n"
            "during_events=_age;_breakup_and_pair;_infect;_stage;"
            "_birth;_death;_report\n"
            "after_events=_no_op\n")

    def post_process(self, dict):
        return super().post_process(dict)

    def run(self, command, key=None):
        strings = ["INITIAL_INFECTIONS", "POP_ALIVE",
                   "INFECT_RATE_ALIVE", "POP_DEAD", "INFECT_RATE_DEAD",
                   "SIMULATION_INFECTIONS",
                   "name;sim;num;date;description;value"]
        strings = "|".join(strings)
        grep_cmd = ["grep", "-E", strings]
        try:
            prog_out = subprocess.Popen(command,
                                        env=self._env,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            grep_out = subprocess.check_output(grep_cmd,
                                               stdin=prog_out.stdout)
            prog_out.wait()
            with open(self._get_output_filename(key), 'w') as f:
                f.write(grep_out.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            logger.error(e)
            with open(self._get_output_filename(key), 'w') as f:
                f.write(prog_out.stderr.read().decode("utf-8"))
        return prog_out

    def _config_filename(self, key):
        return os.path.join(OUTPUT_FILE_DIR, f"faststi_config_{key}.ini")

    def _initial_infections_filename(self, key):
        return os.path.join(DATA_DIR, f"initial_infections_{key}.csv")

    def _mortality_filename(self, key):
        return os.path.join(DATA_DIR, f"mortality_{key}.csv")

    def _infect_filename(self, key):
        return os.path.join(DATA_DIR, f"infect_{key}.csv")

    def write_config_file(self, data, files, key):
        filename = self._config_filename(key)

        # Write initial infections file
        initial_infections_filename = self._initial_infections_filename(key)

        if data["e0_initial_infections_data_source"] == "form":
            fields = [data[k] for k in data if k.startswith("e1_")]
            with open(initial_infections_filename, 'w') as f:
                self._write_initial_gen(f, fields)
        else:
            handle_uploaded_file(files["e2_initial_infections_file"],
                                 initial_infections_filename)

        # Write mortality file
        mortality_filename = self._mortality_filename(key)

        if data["h0_mortality_data_source"] == "form":
            fields = [data[k] for k in data if k.startswith("h1_")]
            with open(mortality_filename, 'w') as f:
                self._write_mortality(f, fields)
        else:
            handle_uploaded_file(files["h2_mortality_file"],
                                 mortality_filename)

        # Write infectiousness file
        infect_filename = self._infect_filename(key)

        if data["k0_infectiousness_data_source"] == "form":
            fields = [data[k] for k in data if k.startswith("k1_")]
            with open(infect_filename, 'w') as f:
                self._write_infect(f, fields)
        else:
            handle_uploaded_file(files["k2_infectiousness_file"],
                                 infect_filename)


        with open(filename, 'w') as f:
            f.write("[Simulation 1]\n")

            # Write fields prefixed with a_ and c_
            for k in filter(lambda x: x.startswith("a_") or
                            x.startswith("c_"), data):
                if k == "a_time_step":
                    val = f'{data[k]} days'
                elif k == "a_simulation_period":
                    val = f'{data[k]} years'
                elif k == "c_start_date":
                    val = f"{data['c_start_date'].year};{data['c_start_date'].month};{data['c_start_date'].day}"
                else:
                    val = data[k]
                o = k[k.find("_")+1:] # Remove identifying prefix
                f.write(f'{o} = {val}\n')
            init_inf_file_suf = Path(self._initial_infections_filename(key)).name
            f.write(f"dataset_gen_infect = {init_inf_file_suf}\n")
            mortality_file_suf = Path(self._mortality_filename(key)).name
            f.write(f"dataset_mortality = {mortality_file_suf}\n")
            infect_file_suf = Path(self._infect_filename(key)).name
            f.write(f"dataset_infect = {infect_file_suf}\n")
            self._write_boiler_plate_config(f, key)
        return filename

    def command_line(self, data, files, key):
        config = self.write_config_file(data, files, key)
        exe = os.path.join(EXE_DIR, EXE_NAME)
        return [exe, "-f", config, ]

    def context_data(self, request, context, **kwargs):
        context = super().context_data(request, context, **kwargs)
        key = context['key']
        if request.method == "POST":
            context['config_files'] = True
            context['config_filename'] = \
                        Path(self._config_filename(key)).name
            context['initial_infection_filename'] = \
                        Path(self._initial_infections_filename(key)).name
            context['mortality_filename'] = \
                        Path(self._mortality_filename(key)).name
            context['infectiousness_filename'] = \
                        Path(self._infect_filename(key)).name
            context['output_filename'] = \
                        Path(self._get_output_filename(key)).name
        return context


def show_config_file(request, slug, path=OUTPUT_FILE_DIR):
    try:
        filename = os.path.join(path, slug)
        f = open(filename, 'r')
        file_content = f.read()
        f.close()
    except FileNotFoundError as e:
        raise Http404(f"File {slug} does not exist.")
    return HttpResponse(file_content, content_type="text/plain")

def show_data_file(request, slug):
    return show_config_file(request, slug, DATA_DIR)

def show_output_file(request, slug):
    return show_config_file(request, slug, OUTPUT_FILE_DIR)
