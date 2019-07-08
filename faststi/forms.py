from django import forms
from django.utils.translation import gettext as _

FILE_OR_FORM = (
    ("form", "Fill in form fields"),
    ("file", "Upload file (advanced)")
)

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
    initial_infections_data_source = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'special'}),
        choices=FILE_OR_FORM, initial="form")

    initial_infections_msm_15_20 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=15 and < 20"),
        initial=0.01)
    initial_infections_msm_20_25 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=20 and < 25"),
        initial=0.03)
    initial_infections_msm_25_30 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=25 and < 30"),
        initial=0.05)
    initial_infections_msm_30_35 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=30 and < 35"),
        initial=0.07)
    initial_infections_msm_35_40 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=35 and < 40"),
        initial=0.07)
    initial_infections_msm_40_45 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=40 and < 45"),
        initial=0.07)
    initial_infections_msm_45_50 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=45 and < 50"),
        initial=0.06)

    initial_infections_file = forms.FileField(
        label=_("Initial infections file"), required=False,
        max_length=500)
