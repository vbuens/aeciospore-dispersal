from django import forms
from django_countries.fields import CountryField
from django_range_slider.fields import RangeSliderField
from django.forms import CheckboxInput, HiddenInput

class InputForm(forms.Form):
    source = forms.IntegerField(label='Source strength (Q= #spores/m/s)', min_value=0, required=False)
    # leaf = RangeSliderField(minimum=1,maximum=100) # without name or label
    # bush = RangeSliderField(minimum=1,maximum=100) # without name or label
    # bush = RangeSliderField(name="%bush",minimum=1,maximum=100) # without name or label
    # infection = forms.IntegerField(label="% infection") # without name or label
    leafperc = forms.CharField(label='leaf-percentage', initial=1, max_length=100,required=True)
    bushperc = forms.CharField(label='bush-percentage', initial=1, max_length=100,required=True)

    height = forms.DecimalField(label='Height of source (default = 1m)',initial=1, min_value=0, max_value=5)

    country = CountryField(blank_label='(select country)').formfield(required=True)
    city = forms.CharField(max_length=200, label='City',required=True)
    # location = forms.BooleanField(required=False, widget=CheckboxInput())
    # cloudiness2 = RangeSliderField(name="%Cloud Cover",minimum=1,maximum=100) # without name or label
    cloudiness = forms.CharField(label='bush-percentage', initial=1, max_length=100, required=False)
    wind = forms.DecimalField(label='Wind speed (in m/s)', min_value=0,required=False)
    choices=[("Low","Low"),("Medium","Medium"),("High","High")]
    UV = forms.ChoiceField(label='UV index', choices=choices,required=False)
    # CHOICES=[('10%'),('20%'),('30%'),('40%'),('50%'),('60%'),('70%'),('80%'),('90%'),('100%')]
    # CHOICES=[('10','10%'),('50','50%'),('100','100%')]
    # CHOICES=[tuple([x,x]) for x in range(10,100,10)]
    # cloudiness = forms.IntegerField(widget=forms.Select(choices=CHOICES),label='% of Cloudiness',required=False)
    # cloudiness = forms.IntegerField(widget=Slider,label='% of Cloudiness',required=False)

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        # self.fields['']
