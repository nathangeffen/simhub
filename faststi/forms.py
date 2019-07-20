from django.utils import timezone
from django import forms
from django.forms import widgets
from django.forms import ValidationError
from django.utils.translation import gettext as _

FILE_OR_FORM = (
    ("form", "Fill in form fields"),
    ("file", "Upload file (advanced)")
)

STAGES = 5

class StageWidget(widgets.MultiWidget):

    def __init__(self, attrs={"min": 0.0, "max": 1.0, "step": "any"}):
        _widgets = (
            widgets.NumberInput(attrs={**attrs, "class": "uninfected"}),
            widgets.NumberInput(attrs={**attrs, "class": "treated"}),
            widgets.NumberInput(attrs={**attrs, "class": "primary"}),
            widgets.NumberInput(attrs={**attrs, "class": "chronic"}),
            widgets.NumberInput(attrs={**attrs, "class": "final"}),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return [None, None, None, None]

    def value_from_datadict(self, data, files, name):
        valuelist = [
            widget.value_from_datadict(data, files, f'{name}_{i}')
            for i, widget in enumerate(self.widgets)]
        if len(valuelist) == STAGES:
            return valuelist
        else:
            return ''

class StageField(forms.MultiValueField):
    widget = StageWidget
    def __init__(self, increasing=False, **kwargs):
        self.increasing = increasing
        error_messages = {
            'incomplete': _('Enter a value for each of the stages.'),
        }
        fields = (
            forms.FloatField(
                error_messages={'incomplete': _('Enter a value.')}
            ),
            forms.FloatField(
                label=_("2"),
                error_messages={'incomplete': _('Enter a value.')}
            ),
            forms.FloatField(
                error_messages={'incomplete': _('Enter a value.')}
            ),
            forms.FloatField(
                error_messages={'incomplete': _('Enter a value.')}
            ),
            forms.FloatField(
                error_messages={'incomplete': _('Enter a value.')}
            )
        )
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, **kwargs
        )

    def compress(self, data_list):
        if len(data_list) != STAGES:
            raise ValidationError(_('Values needed for all stages.'),
                                  code='invalid_stage_value')
        for v in data_list:
            if v < 0.0 or v > 1.0:
                raise ValidationError(_('Values must be between 0 and 1.'),
                                  code='invalid_stage_value')
        if self.increasing:
            prev = data_list[0]
            for v in data_list[1:]:
                if v < prev:
                    raise ValidationError(_('Probabilities cannot decrease '
                                            'between stages'),
                                          code='invalid_stage_value')
                prev = v
        return data_list


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
    c_start_date = forms.DateField(label=_("Start date"),
                                   widget=forms.SelectDateWidget(),
                                   initial=timezone.datetime(2018,1,1))
    c_match_k = forms.IntegerField(label=_("Number of agents to "
                                           "consider for mating"),
                                   min_value=1, max_value=20000,
                                   initial=100)

    # Initial infections

    e0_initial_infections_data_source = forms.ChoiceField(
        label=_("Source of initial infection data"),
        widget=forms.RadioSelect(),
        choices=FILE_OR_FORM, initial="form")

    e1_initial_infections_msm_15_20 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 15 to 20"),
        initial=[0.0, 0.005, 0.006, 0.009, 0.011])
    e1_initial_infections_msm_20_25 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 20 to 25"),
        initial=[0.0, 0.01, 0.015, 0.025, 0.03])
    e1_initial_infections_msm_25_30 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 25 to 30"),
        initial=[0.0, 0.02, 0.025, 0.045, 0.05])
    e1_initial_infections_msm_30_35 = StageField(
        increasing=True,
        label=_("Initial infection rate  MSM age 30 to 35"),
        initial=[0.0, 0.03, 0.035, 0.065, 0.07])
    e1_initial_infections_msm_35_40 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 35 to 40"),
        initial=[0.0, 0.03, 0.035, 0.065, 0.07])
    e1_initial_infections_msm_40_45 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 40 to 45"),
        initial=[0.0, 0.03, 0.035, 0.065, 0.07])
    e1_initial_infections_msm_45_50 = StageField(
        increasing=True,
        label=_("Initial infection rate MSM age 45 to 50"),
        initial=[0.0, 0.03, 0.035, 0.055, 0.06])

    e1_initial_infections_msw_15_20 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 15 to 20"),
        initial=[0.0, 0.005, 0.006, 0.009, 0.01])
    e1_initial_infections_msw_20_25 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 20 to 25"),
        initial=[0.0, 0.01, 0.015, 0.018, 0.02])
    e1_initial_infections_msw_25_30 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 25 to 30"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.025])
    e1_initial_infections_msw_30_35 = StageField(
        increasing=True,
        label=_("Initial infection rate  MSW age 30 to 35"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.025])
    e1_initial_infections_msw_35_40 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 35 to 40"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.025])
    e1_initial_infections_msw_40_45 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 40 to 45"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.025])
    e1_initial_infections_msw_45_50 = StageField(
        increasing=True,
        label=_("Initial infection rate MSW age 45 to 50"),
        initial=[0.0, 0.014, 0.015, 0.018, 0.019])

    e1_initial_infections_wsm_15_20 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 15 to 20"),
        initial=[0.0, 0.005, 0.007, 0.009, 0.011])
    e1_initial_infections_wsm_20_25 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 20 to 25"),
        initial=[0.0, 0.01, 0.015, 0.018, 0.021])
    e1_initial_infections_wsm_25_30 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 25 to 30"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.027])
    e1_initial_infections_wsm_30_35 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 30 to 35"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.028])
    e1_initial_infections_wsm_35_40 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 35 to 40"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.026])
    e1_initial_infections_wsm_40_45 = StageField(
        increasing=True,
        label=_("Initial infection rate WSM age 40 to 45"),
        initial=[0.0, 0.01, 0.015, 0.02, 0.025])
    e1_initial_infections_wsm_45_50 = StageField(
        label=_("Initial infection rate WSM age 45 to 50"),
        initial=[0.0, 0.014, 0.015, 0.018, 0.02])

    e1_initial_infections_wsw_15_20 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 15 to 20"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_20_25 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 20 to 25"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_25_30 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 25 to 30"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_30_35 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 30 to 35"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_35_40 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 35 to 40"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_40_45 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 40 to 45"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])
    e1_initial_infections_wsw_45_50 = StageField(
        increasing=True,
        label=_("Initial infection rate WSW age 45 to 50"),
        initial=[0.0, 0.001, 0.002, 0.003, 0.004])

    e2_initial_infections_file = forms.FileField(
        label=_("Initial infections file"), required=False,
        max_length=500)

    # Mortality rates

    h0_mortality_data_source = forms.ChoiceField(
        label=_("Source of mortality rate data"),
        widget=forms.RadioSelect(),
        choices=FILE_OR_FORM, initial="form")

    h1_mortality_male_15_20 = StageField(
        label=_("Mortality male age 15 to 20"),
        initial=[0.00002, 0.00003, 0.0005, 0.001, 0.003])
    h1_mortality_male_20_25 = StageField(
        label=_("Mortality male age 20 to 25"),
        initial=[0.00002, 0.00003, 0.0005, 0.001, 0.003])
    h1_mortality_male_25_30 = StageField(
        label=_("Mortality male age 25 to 30"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_male_30_35 = StageField(
        label=_("Mortality male age 30 to 35"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_male_35_40 = StageField(
        label=_("Mortality male age 35 to 40"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_male_40_45 = StageField(
        label=_("Mortality male age 40 to 45"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_male_45_50 = StageField(
        label=_("Mortality male age 45 to 50"),
        initial=[0.00001, 0.00002, 0.0006, 0.0015, 0.003])

    h1_mortality_female_15_20 = StageField(
        label=_("Mortality female age 15 to 20"),
        initial=[0.00002, 0.00003, 0.0005, 0.001, 0.003])
    h1_mortality_female_20_25 = StageField(
        label=_("Mortality female age 20 to 25"),
        initial=[0.00002, 0.00003, 0.0005, 0.001, 0.003])
    h1_mortality_female_25_30 = StageField(
        label=_("Mortality female age 25 to 30"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_female_30_35 = StageField(
        label=_("Mortality female age 30 to 35"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_female_35_40 = StageField(
        label=_("Mortality female age 35 to 40"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_female_40_45 = StageField(
        label=_("Mortality female age 40 to 45"),
        initial=[0.00001, 0.00002, 0.0005, 0.001, 0.003])
    h1_mortality_female_45_50 = StageField(
        label=_("Mortality female age 45 to 50"),
        initial=[0.00001, 0.00002, 0.0006, 0.0015, 0.003])

    h2_mortality_file = forms.FileField(
        label=_("Mortality rate file"), required=False,
        max_length=500)

    # Infectiousness rates

    k0_infectiousness_data_source = forms.ChoiceField(
        label=_("Source of infectiousness data"),
        widget=forms.RadioSelect(),
        choices=FILE_OR_FORM, initial="form")

    k1_infectiousness_male_from_male = StageField(
        label=_("Infectiousness male from infected male"),
        initial=[0.0, 0.0, 0.4, 0.16, 0.16])
    k1_infectiousness_male_from_female = StageField(
        label=_("Infectiousness male from infected female"),
        initial=[0.0, 0.0, 0.2, 0.08, 0.08])
    k1_infectiousness_female_from_male = StageField(
        label=_("Infectiousness female from infected male"),
        initial=[0.0, 0.0, 0.24, 0.1, 0.1])
    k1_infectiousness_female_from_female = StageField(
        label=_("Infectiousness female from infected female"),
        initial=[0.0, 0.0, 0.004, 0.003, 0.003])

    k2_infectiousness_file = forms.FileField(
        label=_("Infectiousness rate file"), required=False,
        max_length=500)


    def field_subset(self, prefix):
        return [f for f in self if f.name.startswith(prefix)]

    def clean(self):
        cleaned_data = super().clean()

        # Check the reporting frequency is reasonable
        freq = self.cleaned_data['a_report_frequency']
        per = self.cleaned_data['a_simulation_period']
        step = self.cleaned_data['a_time_step']
        if (365.25 * per / step / freq) > 731:
            raise forms.ValidationError(_("To avoid clogging our server, "
                                          "please increase the period between "
                                          "reports"))

        form_or_file = self.cleaned_data['e0_initial_infections_data_source']
        if form_or_file == "file":
            if self.cleaned_data["e2_initial_infections_file"] is None or \
               self.cleaned_data["e2_initial_infections_file"] == "":
                raise forms.ValidationError(_("Please provide an "
                                              "initial infections file"))
        form_or_file = self.cleaned_data['h0_mortality_data_source']
        if form_or_file == "file":
            if self.cleaned_data["h2_mortality_file"] is None or \
               self.cleaned_data["h2_mortality_file"] == "":
                raise forms.ValidationError(_("Please provide a "
                                              "mortality file"))
        form_or_file = self.cleaned_data['k0_infectiousness_data_source']
        if form_or_file == "file":
            if self.cleaned_data["k2_infectiousness_file"] is None or \
               self.cleaned_data["k2_infectiousness_file"] == "":
                raise forms.ValidationError(_("Please provide an "
                                              "infectiousness file"))
