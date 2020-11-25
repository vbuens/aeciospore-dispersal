from django import forms
from django_countries.fields import CountryField
from django_range_slider.fields import RangeSliderField
from django.forms import CheckboxInput, HiddenInput

class InputForm(forms.Form):
    # Infection level
    choicesleaf=[(0.54,"Low"),(1.82,"Medium"),(5.26,"High",),(17.9,"VeryHigh")]
    leafperc = forms.ChoiceField(label='leaf-percentage', choices=choicesleaf, required=True)
    bushperc = forms.CharField(label='bush-percentage', initial=1, max_length=100,required=True)
    height = forms.DecimalField(label='Height of source (default = 1m)',initial=1, min_value=0, max_value=5)

    #Input weather
    cloudiness = forms.CharField(label='Percentage of cloud cover', initial=1, max_length=100, required=False)
    wind = forms.DecimalField(label='Wind speed (in m/s)', min_value=0,required=False)
    choices=[(100,"Low"),(400,"Medium"),(610,"High")]
    UV = forms.ChoiceField(label='UV index', choices=choices,required=False)
    rain = forms.DecimalField(label='Rainfall rate (mm)',initial=0, min_value=0)

    # Location
    lat= forms.CharField(max_length=200, label='Latitude',required=True)
    NS = forms.ChoiceField(label='Latitude (N-S)', choices=[("+","N"),("-","S")],initial="N")
    lon= forms.CharField(max_length=200, label='Longitude',required=True)
    WE = forms.ChoiceField(label='Longitude (W-E)', choices=[("+","E"),("-","W")],initial="E")

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)


class PredictForm(forms.Form):
    lat= forms.CharField(max_length=200, label='Latitude',required=True)
    NS = forms.ChoiceField(label='Latitude (N-S)', choices=[("+","N"),("-","S")],initial="N")
    lon= forms.CharField(max_length=200, label='Longitude',required=True)
    WE = forms.ChoiceField(label='Longitude (W-E)', choices=[("+","E"),("-","W")],initial="E")

    def __init__(self, *args, **kwargs):
        super(PredictForm, self).__init__(*args, **kwargs)
