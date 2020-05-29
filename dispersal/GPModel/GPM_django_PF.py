
from __future__ import division
import os
import math
import json
import requests
import argparse
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, axes3d
# from .atmospheric_functions import stabilityclass



def stabilityclass_day(u,cloud,UV):
    if (cloud > 0.5): return 'D'
    if UV < 300:
        if (u<2): return 'B'
        if (2<=u<=5): return 'C'
        if (u>5): return 'D'
    elif 300 <= UV <= 600:
        if (u<2): return 'A'
        if 2<=u<5: return 'B'
        if 5<=u<=6: return 'C'
        if u>6: return 'D'
    elif UV > 600:
        if (u<3): return 'A'
        if  (3<=u<=5): return 'B'
        if (u>5): return 'C'

def stabilityclass_night(u,cloud):
    if (cloud > 0.5): return 'D'
    if 0.35<cloud<=0.5:
        if u<=3: return 'F'
        if u<=5: return 'E'
        if u>5: return 'D'
    elif cloud<=0.35:
        if u<=3: return 'E'
        if u>3: return 'D'




def stabilityclass_latlon(lat,lon):
    ''' Calls an API to get weather data from location
        Returns stability class at day and night based on weather'''
    import json
    import requests
        # Gather weather parameters      time='day'
    apikey='a6a267d35d8c445bbc4f74dca9543661'
    url='https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key={}'.format(lat,lon,apikey)
    json_response = requests.get(url).json()

    RH=json_response['data'][0]['rh']
    Irradiance=json_response['data'][0]['solar_rad']
    rain=json_response['data'][0]['precip']
    clouds=(json_response['data'][0]['clouds'])/100
    u=json_response['data'][0]['wind_spd']
    UV=json_response['data'][0]['uv']
    city=json_response['data'][0]['city_name']
    country=json_response['data'][0]['country_code']

    stabilityclasses={}
    stabilityclasses['Day']= stabilityclass_day(u,clouds,Irradiance)
    stabilityclasses['Night']= stabilityclass_night(u,clouds)

    return (stabilityclasses,u,RH,Irradiance,rain,clouds,UV,city, country)


    # altitude = json_response['sun_altitude']
    # urlw = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=3ba98f5e6c66ecde2678c62d5786143b' % city
    # res2 =requests.get(urlw)
    # json_response = res2.json()
    # cloud = float(json_response['clouds']['all'])*0.01
    # u = float(json_response['wind']['speed'])
    # u = float(u) ; cloud=float(cloud) ; altitude=float(altitude)
    #
    # return (stabilityclasses,u)


if os.path.exists('results') == False:
    os.mkdir('results')



## Functions for printing the graph


def graph_2D(allXs,allYs,allCs,stabilityclass,u,time):
    # plt.scatter(allXs,allZs,c=allCs,cmap='nipy_spectral_r') #gist_rainbow') #'gist_ncar') #gist_stern')#'tab20b') YlOrBr')#nipy_spectral_r')#
    plt.scatter(allYs,allXs,c=allCs,cmap='nipy_spectral_r') #gist_rainbow') #'gist_ncar') #gist_stern')#'tab20b') YlOrBr')#nipy_spectral_r')#
    plt.colorbar()
    plt.clim(0,5000)
    # plt.colorbar(p)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Stability class %s. Wind speed: %s m/s' % (stabilityclass,u))
    plt.savefig('dispersal/static/images/results2D_{}.png'.format(time))
    plt.clf()
    # plt.savefig('../static/images/results2D.png')
    # plt.savefig('2D_%s_%s'% (city,time))

def graph_3D(allXs,allYs,allZs,allCs, stability_class,u,time):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    p = ax.scatter(allXs, allYs, allZs, zdir='z', s=20, c=allCs, cmap='nipy_spectral_r', depthshade=True)
    ax.legend()
    fig.colorbar(p)
#    plt.colorbar()
    plt.ylabel('Cross-wind  (m)')
    plt.xlabel('Distance (m)')
#    plt.zlabel('z = Height (m)')
    plt.yticks([0,1,2])
    plt.title('Stability Class: %s. Wind: %s m/s' %(stability_class,u))
#    fig.colorbar(allCs) #, shrink=0.5, aspect=5)
    #plt.zlabel('z')
    plt.savefig('3D_%s_%s'% (city,time))
    # plt.show()



def calculateCs(stability_class,x,y,z,H,Q0,u,I,R):
    Vs=0.0113 # m/s 11.3 mm/s    # Vd=1.27 # Vs=1.23
    z=0
    stabilities={   #a  b   10P     q
        'A': [0.28,0.9,0.527,0.865],
        'B': [0.23,0.85,0.371,0.866],
        'C': [0.22,0.8,0.209,0.897],
        'D': [0.2,0.76,0.128,0.905],
        'E': [0.15,0.73,0.098,0.902],
        'F': [0.12,0.67,0.065,0.902],
      }
    h=0.7
    z0=0.029
    kz0= (10*z0)**(0.53*(x**-0.22))
    d=0.78*h
    a = stabilities[stability_class][0]
    b = stabilities[stability_class][1]
    p = stabilities[stability_class][2]
    q = stabilities[stability_class][3]
    sigy=kz0*p*(x**q)
    sigz=kz0*a*(x**b)
    sig2y=sigy**2
    sig2z=sigz**2
    secondpart=math.exp(-(((H-z)**2)/(2*sig2z)))+math.exp(-(((H+z-2*d)**2)/(2*sig2z)))

    Fs=math.exp(-((I)*x)/5555*u) #5555*u) #18.01
    Yw=0.000272*(R**0.7873)
    Yd1=math.sqrt(2/math.pi)*(Vs/x)
    Y2a=((10*z0)**(0.53*(x**(-0.22))))*(x**(0.22-b+1))
    Y2b=math.log(10*z0)*(0.53*0.22)
    Yd2=Y2a*Y2b/a
    Yd=Yd1*Yd2

    Fd=math.exp((-(Yw+Yd)*x)/u)
    Q=Q0*Fd*Fs
    if Q>Q0:
        print(Q,Yd1,Yd2,Fd,Fs)

    C=(Q/u)*(math.exp((-y**2)/(2*sig2y))/(2*math.pi*sigz*sigy))*secondpart
    return C


def runmodel(graph,H,Q,u,I,R,clouds,stabilityclasses):
    xmax=100.02
    Xlist= np.arange(0.1,xmax,0.1) #Xlist= np.arange(0.001,20,0.001)
    Ylist=np.arange(-5,5,0.1) # Zlist=np.arange(0,H*2,0.1)
    z=0
    times=['Day','Night']
    maxdistances={}
    for time in times:
        allCs=[]
        allXs=[]
        allYs=[]
        for x in Xlist:
            # print(x)
            for y in Ylist:
                # stability_classes= stabilityclass_input(u,clouds,I)
                stabilityclass=stabilityclasses[time]
                C=calculateCs(stabilityclass,x,y,z,H,Q,u,I,R)
    #            R=C*Vd
    #            allRs.append(R)
                allCs.append(C)
                allYs.append(y)
                allXs.append(x)


        graph_2D(allXs,allYs,allCs,stabilityclass,u,time)
        # filename='{}/Cs_{}{}_u{}.csv'.format(output,key,time,u)
        # # writetofile(allXs,allYs,allCs,filename)
        # graphy_2D(allXs,allYs,allCs,stability_class,u,time,key,output)
        Ccum = np.cumsum(allCs)
        max99=max(Ccum)*0.999
        max95=max(Ccum)*0.95
        max75=max(Ccum)*0.75
        max50=max(Ccum)*0.50

        valuesaty0=[]
        for i,x in enumerate(allXs):
            # print(round(allYs[i],2))
            if str(round(allYs[i],2))=="-0.0":
                if allCs[i]<1 and x>1:
                    Xmax=round(x,2)
                    break
        # minC= min(c for c in valuesaty0 if c>1)
        X99 = round(allXs[[n for n,i in enumerate(Ccum) if i> max99][0]],1)
        X95 = round(allXs[[n for n,i in enumerate(Ccum) if i> max95][0]],1)
        X75 = round(allXs[[n for n,i in enumerate(Ccum) if i> max75][0]],1)
        X50 = round(allXs[[n for n,i in enumerate(Ccum) if i> max50][0]],1)
        # Xmin = round(allXs[[n for n,i in enumerate(Ccum) if i== minC][0]],1)
        maxdistances[time]=[X95,X75,X50,X99,Xmax]
    return maxdistances #X95,X75,X50


def runmodel_old(country,city,graph,H,Q, u,stabilityclasses):    # Set up space parameters and empty arrays
    xmax=30
    Xlist= np.arange(0.1,xmax,0.1)
    Zlist=np.arange(0,H*6,0.1)
    # y=0.5
    y=0.01
    allCs=[]
    allXs=[]
    allZs=[]
    # allRs=[]
    maxdistances={}
    times=['Day','Night']
    for time in times:
        allCs=[]
        allXs=[]
        allZs=[]
        allRs=[]
        for x in Xlist:
            for z in Zlist:
                stability_class= stabilityclasses[time]
                stabilities={   #sigy                   sigz
                    'A': [0.22*x*((1+0.0001*x)**(-0.5)),0.2*x],
                    'B': [0.16*x*((1+0.0001*x)**(-0.5)),0.12*x],
                    'C': [0.11*x*((1+0.0001*x)**(-0.5)),0.08*x*((1+0.002*x)**(-0.5))],
                    'D': [0.08*x*((1+0.0001*x)**(-0.5)),0.06*x*((1+0.0015*x)**(-0.5))],
                    'E': [0.06*x*((1+0.0001*x)**(-0.5)),0.03*x*((1+0.0003*x)**(-1))],
                    'F': [0.04*x*((1+0.0001*x)**(-0.5)),0.016*x*((1+0.0003*x)**(-1))],
                  }
                sigy=stabilities[stability_class][0]
                sigz=stabilities[stability_class][1]
                sig2y=sigy**2
                sig2z=sigz**2

                secondpart=math.exp(-(((H-z)**2)/(2*sig2z)))+math.exp(-(((H+z)**2)/(2*sig2z)))
                C=(Q/u)*(math.exp((-y**2)/(2*sig2y))/(2*math.pi*sigz*sigy))*secondpart

        #            R=C*Vd
        #            allRs.append(R)
                allCs.append(C)
                allZs.append(z)
                allXs.append(x)

        # print('''Location:%s,%s\nWind Speed: %.2f\nCloudiness: %.2f\nTime: %s\nSun Altitude: %.2f\nStability Class: %s\nQ: %.2f\nSource height: %.1f\n\n''' % (city,country,u,cloud,time,altitude,stability_class,Q,H))
        if graph=='2D':
            plt.clf()
            #graph_2D(allXs,allZs,allCs,stability_class,u,time)
            plt.scatter(allXs,allZs,c=allCs,cmap='nipy_spectral_r') #gist_rainbow') #'gist_ncar') #gist_stern')#'tab20b') YlOrBr')#nipy_spectral_r')#
            plt.colorbar()
            # plt.colorbar(p)
            plt.xlabel('Distance (m)')
            plt.ylabel('Height (m)')
            plt.title('Stability class %s. Wind speed: %s m/s. %s time.' % (stability_class,u, time))

            plt.savefig(f'dispersal/static/images/results2D_{time}.png')
            plt.clf()

        elif graph == '3D':
            graph_3D(allXs,allYs,allZs,allCs, stability_class,u,time)

        Ccum = np.cumsum(allCs)
        max95=max(Ccum)*0.95
        max75=max(Ccum)*0.75
        max50=max(Ccum)*0.50
        X95 = round(allXs[[n for n,i in enumerate(Ccum) if i> max95][0]],1)
        X75 = round(allXs[[n for n,i in enumerate(Ccum) if i> max75][0]],1)
        X50 = round(allXs[[n for n,i in enumerate(Ccum) if i> max50][0]],1)
        maxdistances[time]=[X95,X75,X50]
    return maxdistances #X95,X75,X50


def get_time():
    datetime.now(pytz.timezone('Europe/London')).strftime("%H:%M")
