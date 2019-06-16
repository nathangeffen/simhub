from django import forms
from django.utils.translation import gettext as _


class GamblerForm(forms.Form):
    start_amount = forms.IntegerField(label="Initial amount of money per gambler",
                                      min_value=1, max_value=200, initial=10)
    num_tests = forms.IntegerField(label=_("Number of tests"),
                                   min_value=1, max_value=5000, initial=500)
    num_gambles = forms.IntegerField(label=_("Number of gambles per test"),
                                     min_value=1, max_value=100000, initial=10000)
    num_players = forms.IntegerField(label="Number of players per test",
                                     min_value=1, max_value=100, initial=10)
