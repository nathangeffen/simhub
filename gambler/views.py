"""
Views for gambling simulation
"""

import os

from django.conf import settings

from scheduler.views import JobFormView, JobJSONView
from .management.commands import sim_gamblers
from .forms import GamblerForm


class GamblerFormView(JobFormView):
    template_name = 'gambler/gambler_form.html'
    form_class = GamblerForm

    def command_line(self, data, files, key):
        exe = os.path.join(settings.BASE_DIR,
                           'gambler/management/commands/sim_gamblers.py')
        amount = str(data['start_amount'])
        runs = str(data['num_tests'])
        gambles = str(data['num_gambles'])
        players = str(data['num_players'])
        filename = self.get_output_filename()
        return ["python3",
                exe,
                f"--amount={amount}",
                f"--runs={runs}",
                f"--gambles={gambles}",
                f"--players={players}",
                f"--output={filename}", ]
