"""
Views for faststi simulation
"""

import os
import subprocess
from scheduler.views import JobFormView
from scheduler.settings import OUTPUT_FILE_DIR, TIMEOUT
from .settings import DATA_DIR, EXE_DIR, EXE_NAME
from .forms import FaststiForm


class FaststiFormView(JobFormView):
    template_name = 'faststi/faststi_form.html'
    form_class = FaststiForm

    def __init__(self):
        super(FaststiFormView, self).__init__()
        self.set_env("FSTI_DATA", DATA_DIR)

    def _write_boiler_plate_config(self, f, key):
            # f.write(f"results_file = " +
            #         self._get_output_filename(key) + "\n")
            f.write(
                "dataset_gen_sex=dataset_gen_sex.csv\n"
                "dataset_gen_sex_preferred=dataset_gen_sex_preferred.csv\n"
                "dataset_gen_infect=dataset_gen_infect.csv\n"
                "dataset_gen_treated=dataset_gen_treated.csv\n"
                "dataset_gen_resistant=dataset_gen_resistant.csv\n"
                "dataset_gen_mating=dataset_gen_mating.csv\n"
                "dataset_birth_infect=dataset_gen_infect.csv\n"
                "dataset_birth_treated=dataset_birth_treated.csv\n"
                "dataset_birth_resistant=dataset_birth_resistant.csv\n"
                "dataset_rel_period=dataset_rel.csv\n"
                "dataset_single_period=dataset_single.csv\n"
                "dataset_infect=dataset_infect.csv\n"
                "dataset_infect_stage=dataset_infect_stage.csv\n"
                "dataset_mortality=dataset_mortality_simple.csv\n"
                "before_events=_write_results_csv_header;"
                "_generate_and_pair;_report\n"
                "during_events=_age;_breakup_and_pair;_infect;_stage;"
                "_birth;_death;_report\n"
                "after_events=_report\n")

    def post_process(self, dict):
        return super().post_process(dict)

    def run(self, command, key=None):
        strings = ["INITIAL_INFECTIONS", "POP_ALIVE",
                   "INFECT_RATE_ALIVE", "POP_DEAD", ]
        strings = "|".join(strings)
        grep_cmd = ["grep", "-E", strings]
        prog_out = subprocess.Popen(command,
                                    env=self._env, stdout=subprocess.PIPE)
        grep_out = subprocess.check_output(grep_cmd,
                                           stdin=prog_out.stdout)
        prog_out.wait()
        with open(self._get_output_filename(key), 'w') as f:
            f.write(grep_out.decode("utf-8"))
        return prog_out

    def write_config_file(self, data, key):
        filename = os.path.join(OUTPUT_FILE_DIR,
                                f"faststi_config_{key}.ini")
        with open(filename, 'w') as f:
            f.write("[Simulation 1]\n")
            for k in data:
                if k == "time_step":
                    val = f'{data[k]} days'
                elif k == "simulation_period":
                    val = f'{data[k]} years'
                else:
                    val = data[k]
                f.write(f'{k} = {val}\n')
            self._write_boiler_plate_config(f, key)
        return filename

    def command_line(self, data, key):
        config = self.write_config_file(data, key)
        exe = os.path.join(EXE_DIR, EXE_NAME)
        return [exe, "-f", config, ]
