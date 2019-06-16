from django import forms
from django.utils.translation import gettext as _


class FaststiForm(forms.Form):
    num_agents = forms.IntegerField(label=_("Number of agents"),
                                    min_value=50, max_value=20000,
                                    initial=10000)
    time_step = forms.IntegerField(label=_("Size of simulation "
                                           "iteration in days"),
                                   min_value=1, max_value=366,
                                   initial=1)
    simulation_period = forms.IntegerField(label=_("Period of simulation "
                                                   "in years"),
                                           min_value=1, max_value=20,
                                           initial=10)
    report_frequency = forms.IntegerField(label=_("Report every how "
                                                  "many iterations"),
                                          min_value=1, max_value=20000,
                                          initial=10)
    match_k = forms.IntegerField(label=_("Number of agents to "
                                         "consider for mating"),
                                 min_value=1, max_value=20000,
                                 initial=100)
