
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

# Parse arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('-Q','--sourcestrength', default=948372.0863 , type=float,nargs='?', help = 'Source Strength: spores/(s m)')
# parser.add_argument('-y','--y',type=float,default=0,help = 'Distance in the cross-wind direction to the source: y (m)')
# parser.add_argument('-xmax','--xmax',type=float,default=50,help = 'Maximum horizontal distance from the source: x (m)')
# parser.add_argument('-H','--height',type=float,default=1,help = 'Height of the source: H (m)')
# # parser.add_argument('-vd','--depositionvelocity',type=float,default=1.27,help = 'Deposition velocity of spores: Vd (m)')
# # parser.add_argument('-zmax','--zmax',type=float,default=6,help = 'Maximum height from the source: z (m)')
# parser.add_argument('-u','--wind', type=float, default=8, help = 'Wind velocity: u. Default 8 (m/s)')
# parser.add_argument('-cn','--country', type=str, help = 'Wind velocity: u (m/s)', required= True)
# parser.add_argument('-ct','--city', type=str, help = 'Wind velocity: u (m/s)', required= True)
# parser.add_argument('-g','--graph', type=str, help = 'Type of Graph (3D or 2D). Default: 2D', default= '2D')
#
# args = parser.parse_args()
# Q = args.sourcestrength
# y = args.y
# xmax = args.xmax
# H = args.height
# u = args.wind
# country = args.country
# city = args.city
# graph = args.graph

if os.path.exists('results') == False:
    os.mkdir('results')



## Functions for printing the graph


def graph_2D(allXs,allZs,allCs,stabilityclass,u,time):
    plt.scatter(allXs,allZs,c=allCs,cmap='nipy_spectral_r') #gist_rainbow') #'gist_ncar') #gist_stern')#'tab20b') YlOrBr')#nipy_spectral_r')#

   # plt.colorbar()
    # plt.colorbar(p)
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Stability class %s. Wind speed: %s m/s' % (stability_class,u))
    plt.savefig('../static/images/results2D.png')
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

def stabilityclass(u,time,cloud,altitude):
    u=float(u) ; cloud=float(cloud) ; altitude=float(altitude)
    if time=='night':
        if cloud>0.5:
            return 'D'
        elif 0.35<cloud<=0.5:
            if u<=3:
                return 'F'
            elif u<=5:
                return 'E'
            elif u>5:
                return 'D'
        elif cloud<=0.35:
            if u<=3:
                return 'E'
            else:
                return 'D'

    elif time=='day':
        if cloud>0.5:
            return 'D'
        elif altitude<35:
            if u<2:
                return 'B'
            elif 2<=u<=5:
                return 'C'
            elif 5<u:
                return 'D'
        elif 35<=altitude<=60:
            if u<2:
                return 'A'
            elif 2<=u<5:
                return 'B'
            elif 5<=u<=6:
                return 'C'
            elif 6<u:
                return 'D'

        elif altitude>60:
            if u<3:
                return 'A'
            elif 3<=u<=5:
                return 'B'
            elif 5<u:
                return 'C'


def runmodel(country,city,graph,H,Q, u,stabilityclasses):
    print(u)
    # Set up space parameters and empty arrays
    xmax=50
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
            # plt.clf()
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
