from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InputForm, PredictForm
from .GPModel.GPM_django_PF import runmodel, stabilityclass_latlon, stabilityclass_input
from .GPModel.releaseprediction import RH_APIcall

def index(request):
    return render(request, 'dispersal/index.html')

def about(request):
    return render(request, 'dispersal/about.html')
def run(request):
    template_name = 'dispersal/run.html'
    form = InputForm()
    return render(request, template_name, {'form': form})

def release(request):
    template_name = 'dispersal/prediction.html'
    form = PredictForm()
    return render(request, template_name, {'form': form})

def predictions(request):
    if request.method == 'POST':
        form = PredictForm(request.POST)
        if form.is_valid():
            lat = form.cleaned_data['lat']
            NS = form.cleaned_data['NS']
            lon = form.cleaned_data['lon']
            WE = form.cleaned_data['WE']
            lat=float(NS+lat)
            lon=float(WE+lon)
            prediction,city,country=RH_APIcall(lat,lon)
            return render(request, 'dispersal/prediction_results.html', {'context':prediction,'city':city,'country':country})
    else:
        return redirect('/dispersal/predictions')
        # return render(request, 'dispersal/prediction.html')

def results(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            graph='2D'
            lat = form.cleaned_data['lat']
            NS = form.cleaned_data['NS']
            lon = form.cleaned_data['lon']
            WE = form.cleaned_data['WE']
            lat=float(NS+lat)
            lon=float(WE+lon)

            if request.GET.get('weathercheck') == "on":
                UV = form.cleaned_data['UV']
                wind = form.cleaned_data['wind']
                cloudiness =  int(form.cleaned_data['cloudperc'])/100
                #cloudiness =  int(request.GET.get('cloudperc'))/100
                stabilityclasses=stabilityclass_input(wind,cloudiness,UV)

            else:
                stabilityclasses,wind,RH,I,R,clouds,UV,city, country =stabilityclass_latlon(lat,lon)

            H = float(form.cleaned_data['height'])
            bushperc = int(form.cleaned_data['bushperc'])/100
            leafperc = float(form.cleaned_data['leafperc'])/100
            # Calculating the source strength based on percentage of infection
            # 8.29 cups/mm * leaf area * %infection in leaf * spores/cup
            # sporesinleaf = 8.29* 9.93 * leafperc * 7111.37
            sporesinleaf = 585409.48 * leafperc
            # Number of leaves in bush * % bush infected
            leafinbush= 900* bushperc
            # spores in lef * leaves in bush * % germination
            Q= round(sporesinleaf*leafinbush*0.6*0.5,2)
            # Q = round(623909.0877*0.6*bushperc*leafperc,2)

            maxdistances=runmodel(graph,H,Q, float(wind),I,R,clouds,stabilityclasses)
            context={'source':Q,'country':country,'city':city,
                    'rain': R,'RH': RH,'clouds':round(clouds*100,1),'Irradiance': I,
                    'wind': wind, 'bushperc': round(bushperc*100,0), 'leafperc': leafperc*100,
                    'X99d': maxdistances['Day'][3],'X99n': maxdistances['Night'][3],
                    'XminD': maxdistances['Day'][4],'XminN': maxdistances['Night'][4],
                    'X95d': maxdistances['Day'][0],'X75d': maxdistances['Day'][1],
                    'X50d': maxdistances['Day'][2],'X95n': maxdistances['Night'][0],
                    'X75n': maxdistances['Night'][1],'X50n': maxdistances['Night'][2]}
            return render(request, 'dispersal/results.html', context)
        else:
            print('form no valid')
            form = InputForm()
            return redirect('/dispersal/run/')
            # return render(request,'dispersal/run.html', {'form': form})
    else:
        return redirect('/dispersal/run/')
