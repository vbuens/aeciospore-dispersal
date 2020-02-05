
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
from atmospheric_functions import stabilityclass

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-Q','--sourcestrength', default=948372.0863 , type=float,nargs='?', help = 'Source Strength: spores/(s m)')
parser.add_argument('-y','--y',type=float,default=0,help = 'Distance in the cross-wind direction to the source: y (m)')
parser.add_argument('-xmax','--xmax',type=float,default=50,help = 'Maximum horizontal distance from the source: x (m)')
parser.add_argument('-H','--height',type=float,default=1,help = 'Height of the source: H (m)')
# parser.add_argument('-vd','--depositionvelocity',type=float,default=1.27,help = 'Deposition velocity of spores: Vd (m)')
# parser.add_argument('-zmax','--zmax',type=float,default=6,help = 'Maximum height from the source: z (m)')
parser.add_argument('-u','--wind', type=float, default=8, help = 'Wind velocity: u. Default 8 (m/s)')
parser.add_argument('-cn','--country', type=str, help = 'Wind velocity: u (m/s)', required= True)
parser.add_argument('-ct','--city', type=str, help = 'Wind velocity: u (m/s)', required= True)
parser.add_argument('-g','--graph', type=str, help = 'Type of Graph (3D or 2D). Default: 2D', default= '2D')

args = parser.parse_args()
Q = args.sourcestrength
y = args.y
xmax = args.xmax
H = args.height
u = args.wind
country = args.country
city = args.city
graph = args.graph

if os.path.exists('results') == False:
    os.mkdir('results')

# Gather weather parameters      time='day'
url = 'https://api.ipgeolocation.io/astronomy?apiKey=00424bbd52cf442ea1e923480323e6c7&tz=%s/%s' % (country,city)
res =requests.get(url,params={'q':'requests+language:python'})
json_response = res.json()
altitude = json_response['sun_altitude']
urlw = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=3ba98f5e6c66ecde2678c62d5786143b' % city
res2 =requests.get(urlw)
json_response = res2.json()
print
cloud = float(json_response['clouds']['all'])*0.01

u = float(json_response['wind']['speed'])
# Set up space parameters and empty arrays
Xlist= np.arange(0.1,xmax,0.1)
Zlist=np.arange(0,H*6,0.1)
y=0.5
allCs=[]
allXs=[]
allZs=[]
# allRs=[]



## Functions for printing the graph


def graph_2D(allXs,allZs,allCs,stabilityclass,u,time):
    plt.scatter(allXs,allZs,c=allCs,cmap='nipy_spectral_r') #gist_rainbow') #'gist_ncar') #gist_stern')#'tab20b') YlOrBr')#nipy_spectral_r')#

   # plt.colorbar()
    # plt.colorbar(p)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Stability class %s. Wind speed: %s m/s' % (stability_class,u))
    # plt.savefig('$s/Q%i_y%s_wind%s'% (path,Q,y,u))
    plt.savefig('3D_%s_%s'% (city,time))

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


def run_model2222(country,city,graph,H,Q):

    # from .atmospheric_functions import stabilityclass

    # Gather weather parameters      time='day'
    url = 'https://api.ipgeolocation.io/astronomy?apiKey=00424bbd52cf442ea1e923480323e6c7&tz=%s/%s' % (country,city)
    res =requests.get(url,params={'q':'requests+language:python'})
    json_response = res.json()
    altitude = json_response['sun_altitude']
    urlw = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=3ba98f5e6c66ecde2678c62d5786143b' % city
    res2 =requests.get(urlw)
    json_response = res2.json()
    # print
    cloud = float(json_response['clouds']['all'])*0.01

    u = float(json_response['wind']['speed'])
    # Set up space parameters and empty arrays
    xmax=50
    Xlist= np.arange(0.1,xmax,0.1)
    Zlist=np.arange(0,H*6,0.1)
    # y=0.5
    y=0.1
    allCs=[]
    allXs=[]
    allZs=[]
    # allRs=[]

    times=['Day','Night']
    for time in times:
        allCs=[]
        allXs=[]
        allZs=[]
        allRs=[]
        for x in Xlist:
            for z in Zlist:
                stability_class= stabilityclass(u,time,cloud,altitude)
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

        print('''Location:%s,%s\nWind Speed: %.2f\nCloudiness: %.2f\nTime: %s\nSun Altitude: %.2f\nStability Class: %s\nQ: %.2f\nSource height: %.1f\n\n''' % (city,country,u,cloud,time,altitude,stability_class,Q,H))
        if graph=='2D':
            plt.clf()
            # graph_2D(allXs,allZs,allCs,stability_class,u,time)
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




times=['day','night']
for time in times:
    allCs=[]
    allXs=[]
    allZs=[]
    allRs=[]
    for x in Xlist:
        for z in Zlist:
            stability_class= stabilityclass(u,time,cloud,altitude)
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

    print('''Location:%s,%s\nWind Speed: %.2f\nCloudiness: %.2f\nTime: %s\nSun Altitude: %.2f\nStability Class: %s\nQ: %.2f\nSource height: %.1f\n\n''' % (city,country,u,cloud,time,altitude,stability_class,Q,H))
    if graph=='2D':
        graph_2D(allXs,allZs,allCs,stabilityclass,u,time)
    elif graph == '3D':
        graph_3D(allXs,allYs,allZs,allCs, stability_class,u,time)



def get_time():
    datetime.now(pytz.timezone('Europe/London')).strftime("%H:%M")
