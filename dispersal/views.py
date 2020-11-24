from django.shortcuts import render, redirect
from .forms import InputForm, PredictForm
from .GPModel.GPM_django_PF import runmodel, stabilityclass_latlon, stabilityclass_input
from .GPModel.releaseprediction import RH_APIcall
from .models import EntryRequest

def index(request):
    return render(request, 'dispersal/index.html')
def about(request):
    return render(request, 'dispersal/about.html')
def entries(request):
    context ={'database' : EntryRequest.objects.all()}
    return render(request, 'dispersal/database.html', context )

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

def results(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            graph='2D'
            lat = form.cleaned_data['lat']
            NS = form.cleaned_data['NS']
            lon = form.cleaned_data['lon']
            WE = form.cleaned_data['WE']
            location=str(NS+lat)+' , '+str(WE+lon)
            lat=float(NS+lat)
            lon=float(WE+lon)

            if request.GET.get('weathercheck') == "on":
                print('INPUT DATA!!!!!!!!!')
                I = form.cleaned_data['UV']
                wind = form.cleaned_data['wind']
                cloudiness =  int(form.cleaned_data['cloudperc'])/100
                stabilityclasses=stabilityclass_input(wind,cloudiness,I)

            else:
                try:
                    stabilityclasses,wind,RH,I,R,clouds,UV,city, country =stabilityclass_latlon(lat,lon)
                except Exception:
                    message='It seems like there has been an error regarding the API that gathers weather data.\nYou can try again later or run the model inputting yourself the weather data.'
                    return render(request,'dispersal/error.html',{'exception':message})

            H = float(form.cleaned_data['height'])
            bushperc = int(form.cleaned_data['bushperc'])/100
            leafperc = float(form.cleaned_data['leafperc'])/100
            # Calculating the source strength based on percentage of infection
            # sporesinleaf = 8.29* 993 mm2 * 7111.37 = 58540948.1 spores in leaf
            # Q(spores/s) =58540948.1 * 0.0296 (% released)/3600 (s) = 481.34
            sporesinleaf = 481.34 * leafperc
            # Number of leaves in bush (approx 1m2)* % bush infected
            leafinbush= 900* bushperc
            Q= round(sporesinleaf*leafinbush,2)

            try:
                maxdistances=runmodel(graph,H,Q, float(wind),I,R,clouds,stabilityclasses)
            except Exception as e:
                message="There has been an error with running the model. Maintance might be needed."
                return render(request,'dispersal/error.html',{'exception':message})

            entry = EntryRequest(country=country, city=city,bushperc=bushperc*100,leafperc=leafperc*100,
                    height=H,Q=Q,stability_class=stabilityclasses,rain=R,RH=RH,irradiance=UV,
                    wind=wind, location=location,maxdis=max([maxdistances['Day'][4],maxdistances['Night'][4]]))
            entry.save()

            context={'source':Q,'country':country,'city':city,
                    'rain': R,'RH': RH,'clouds':round(clouds*100,1),'Irradiance': I,
                    'wind': wind, 'bushperc': round(bushperc*100,0), 'leafperc': leafperc*100,
                    'X99d': maxdistances['Day'][3],'X99n': maxdistances['Night'][3],
                    'XminD': maxdistances['Day'][4],'XminN': maxdistances['Night'][4],
                    'X95d': maxdistances['Day'][0],'X75d': maxdistances['Day'][1],
                    'X50d': maxdistances['Day'][2],'X95n': maxdistances['Night'][0],
                    'X75n': maxdistances['Night'][1],'X50n': maxdistances['Night'][2],
                    'imgday': maxdistances['Day'][5].decode('utf-8'),'imgnight':maxdistances['Night'][5].decode('utf-8')}
            return render(request, 'dispersal/results.html', context)
        else:
            print('form no valid')
            form = InputForm()
            return redirect('/dispersal/run/')

    else:
        return redirect('/dispersal/run/')
