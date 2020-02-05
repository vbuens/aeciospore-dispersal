from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm
from .GPModel.GPM_django import runmodel
from django_countries import countries
from .GPModel.atmospheric_functions import stabilityclass_input, stabilityclass_API
# Create your views here.

def index(request):
    return render(request, 'dispersal/index.html') #"Hello, world. You're at the model index. Go to run model")

def about(request):
    return render(request, 'dispersal/about.html') #"Hello, world. You're at the model index. Go to run model")

def run(request):
    template_name = 'dispersal/run.html'
    form = InputForm()
    return render(request, template_name, {'form': form})

def results(request):
    print('works')

    if request.method == 'POST':
        return render(request, 'dispersal/run.html')
    else:
        form = InputForm(request.GET)
        if form.is_valid():
            # Q=form.cleaned_data['source'] #source strength
            graph='2D'
            country = form.cleaned_data['country']
            country=dict(countries)[country].strip(' ')
            city = form.cleaned_data['city']


            if request.GET.get('weathercheck') == "on":
                UV = form.cleaned_data['UV']
                wind = form.cleaned_data['wind']
                cloudiness =  int(request.GET.get('cloudperc'))/100
                stabilityclasses=stabilityclass_input(wind,cloudiness,UV)

            else:
                stabilityclasses,wind = stabilityclass_API(city,country)

            H = float(form.cleaned_data['height'])
            bushperc = int(request.GET.get('bushperc'))/100
            leafperc = int(request.GET.get('leafperc'))/100
            print(stabilityclasses, wind)
            # Calculating the source strength based on percentage of infection
            Q = round(34661.61598*bushperc*leafperc,2)
            print(Q)
            maxdistances=runmodel(country,city,graph,H,Q, float(wind),stabilityclasses)
            context={'source':Q,'country':country,'city':city,
                    'wind': wind, 'bushperc': round(bushperc*100,0), 'leafperc': round(leafperc*100),
                    'X95d': maxdistances['Day'][0],'X75d': maxdistances['Day'][1],
                    'X50d': maxdistances['Day'][2],'X95n': maxdistances['Night'][0],
                    'X75n': maxdistances['Night'][1],'X50n': maxdistances['Night'][2]}
            return render(request, 'dispersal/results.html', context)
        else:
            return render(request,'dispersal/run.html', {'form': form})
