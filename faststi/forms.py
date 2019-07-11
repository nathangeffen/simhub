from django import forms
from django.utils.translation import gettext as _

FILE_OR_FORM = (
    ("form", "Fill in form fields"),
    ("file", "Upload file (advanced)")
)

class FaststiForm(forms.Form):
    a_num_agents = forms.IntegerField(label=_("Number of agents"),
                                      min_value=50, max_value=20000,
                                      initial=10000)
    a_time_step = forms.IntegerField(label=_("Size of simulation "
                                             "iteration in days"),
                                     min_value=1, max_value=366,
                                     initial=1)
    a_simulation_period = forms.IntegerField(label=_("Period of simulation "
                                                     "in years"),
                                             min_value=1, max_value=20,
                                             initial=10)
    a_report_frequency = forms.IntegerField(label=_("Report every how "
                                                    "many iterations"),
                                            min_value=1, max_value=20000,
                                            initial=10)
    c_match_k = forms.IntegerField(label=_("Number of agents to "
                                           "consider for mating"),
                                   min_value=1, max_value=20000,
                                   initial=100)
    e0_initial_infections_data_source = forms.ChoiceField(
        label=_("Source of initial infection data"),
        widget=forms.RadioSelect(),
        choices=FILE_OR_FORM, initial="form")

    e1_initial_infections_msm_15_20 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=15 and < 20"),
        initial=0.01)
    e1_initial_infections_msm_20_25 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=20 and < 25"),
        initial=0.03)
    e1_initial_infections_msm_25_30 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=25 and < 30"),
        initial=0.05)
    e1_initial_infections_msm_30_35 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=30 and < 35"),
        initial=0.07)
    e1_initial_infections_msm_35_40 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=35 and < 40"),
        initial=0.07)
    e1_initial_infections_msm_40_45 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=40 and < 45"),
        initial=0.07)
    e1_initial_infections_msm_45_50 = forms.FloatField(
        label=_("Initial infection rate of MSM age >=45 and < 50"),
        initial=0.06)

    e1_initial_infections_msw_15_20 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=15 and < 20"),
        initial=0.01)
    e1_initial_infections_msw_20_25 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=20 and < 25"),
        initial=0.02)
    e1_initial_infections_msw_25_30 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=25 and < 30"),
        initial=0.02)
    e1_initial_infections_msw_30_35 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=30 and < 35"),
        initial=0.01)
    e1_initial_infections_msw_35_40 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=35 and < 40"),
        initial=0.01)
    e1_initial_infections_msw_40_45 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=40 and < 45"),
        initial=0.01)
    e1_initial_infections_msw_45_50 = forms.FloatField(
        label=_("Initial infection rate of MSW age >=45 and < 50"),
        initial=0.01)

    e1_initial_infections_wsm_15_20 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=15 and < 20"),
        initial=0.01)
    e1_initial_infections_wsm_20_25 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=20 and < 25"),
        initial=0.02)
    e1_initial_infections_wsm_25_30 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=25 and < 30"),
        initial=0.03)
    e1_initial_infections_wsm_30_35 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=30 and < 35"),
        initial=0.02)
    e1_initial_infections_wsm_35_40 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=35 and < 40"),
        initial=0.02)
    e1_initial_infections_wsm_40_45 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=40 and < 45"),
        initial=0.02)
    e1_initial_infections_wsm_45_50 = forms.FloatField(
        label=_("Initial infection rate of WSM age >=45 and < 50"),
        initial=0.02)

    e1_initial_infections_wsw_15_20 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=15 and < 20"),
        initial=0.00)
    e1_initial_infections_wsw_20_25 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=20 and < 25"),
        initial=0.01)
    e1_initial_infections_wsw_25_30 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=25 and < 30"),
        initial=0.01)
    e1_initial_infections_wsw_30_35 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=30 and < 35"),
        initial=0.01)
    e1_initial_infections_wsw_35_40 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=35 and < 40"),
        initial=0.01)
    e1_initial_infections_wsw_40_45 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=40 and < 45"),
        initial=0.01)
    e1_initial_infections_wsw_45_50 = forms.FloatField(
        label=_("Initial infection rate of WSW age >=45 and < 50"),
        initial=0.01)

    e2_initial_infections_file = forms.FileField(
        label=_("Initial infections file"), required=False,
        max_length=500)

    def field_subset(self, prefix):
        return [f for f in self if f.name.startswith(prefix)]

    def clean(self):
        cleaned_data = super().clean()
        form_or_file = self.cleaned_data['e0_initial_infections_data_source']
        if form_or_file == "file":
            if self.cleaned_data["e2_initial_infections_file"] is None or \
               self.cleaned_data["e2_initial_infections_file"] == "":
                raise forms.ValidationError(_("Please provide an "
                                              "initial infections file"))
