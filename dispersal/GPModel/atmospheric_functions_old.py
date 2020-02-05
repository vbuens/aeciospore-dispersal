#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:47:28 2018

@author: buenov
"""

# u = wind speed
# time = day or night
# cloud = 0-1 (% of the sky that is covered)
# Solar radiation = W/m2
def stabilityclass_rad(u,time,cloud,rad):
    print('WHAT')
    u=float(u) ; cloud=float(cloud) ; rad=float(rad)
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
        elif rad<300:
            if u<2:
                return 'B'
            elif 2<=u<=5:
                return 'C'
            elif 5<u:
                return 'D'
        elif 300<=rad<=600:
            if u<2:
                return 'A'
            elif 2<=u<5:
                return 'B'
            elif 5<=u<=6:
                return 'C'
            elif 6<u:
                return 'D'

        elif rad>600:
            if u<3:
                return 'A'
            elif 3<=u<=5:
                return 'B'
            elif 5<u:
                return 'C'

def stabilityclass(u,time,cloud,altitude):
    u=float(u) ; cloud=float(cloud) ; altitude=float(altitude)
    if time=='Night':
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

    elif time=='Day':
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

def stabilityclass_input2(u,time,cloud,rad):
    print('WHAT')
    u=float(u) ; cloud=float(cloud) ; rad=float(rad)
    if time=='Night':
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

    elif time=='Day':
        if cloud>0.5:
            return 'D'
        elif UV == "Low":
            if u<2:
                return 'B'
            elif 2<=u<=5:
                return 'C'
            elif 5<u:
                return 'D'
        elif UV == "Medium":
            if u<2:
                return 'A'
            elif 2<=u<5:
                return 'B'
            elif 5<=u<=6:
                return 'C'
            elif 6<u:
                return 'D'
        elif UV == "High":
            if u<3:
                return 'A'
            elif 3<=u<=5:
                return 'B'
            elif 5<u:
                return 'C'

def stabilityclass_inputday(u,cloud,UV):
    if cloud>0.5:
        return 'D'
    elif UV == "Low":
        if u<2:
            return 'B'
        elif 2<=u<=5:
            return 'C'
        elif 5<u:
            return 'D'
    elif UV == "Medium":
        if u<2:
            return 'A'
        elif 2<=u<5:
            return 'B'
        elif 5<=u<=6:
            return 'C'
        elif 6<u:
            return 'D'
    elif UV == "High":
        if u<3:
            return 'A'
        elif 3<=u<=5:
            return 'B'
        elif 5<u:
            return 'C'
def stabilityclass_inputnight(u,cloud):
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

def stabilityclass_input(u,cloud,UV):
    u=float(u) ; cloud=float(cloud)
    stabilityclasses={}
    stabilityclasses['Day']= stabilityclass_inputday(u,UV,cloud)
    stabilityclasses['Night']= stabilityclass_inputday(u,cloud)

def radiation(season,weather,time='notmidday'):
    if weather=='cloudy':
        return 'overcast'
    elif weather=='sunny':
        if season=='winter':
            return 'slight' #>300W/m2
        elif season=='summer':
            if time=='midday':
                return 'strong'  #>600W/m2
            else:
                return 'moderate' #300-600W/m2
def radiation(season,weather,time='notmidday'):
    if weather=='cloudy':
        return 'overcast'
    elif weather=='sunny':
        if season=='winter':
            return 'slight' #>300W/m2
        elif season=='summer':
            if time=='midday':
                return 'strong'  #>600W/m2
            else:
                return 'moderate' #300-600W/m2
