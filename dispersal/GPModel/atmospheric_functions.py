#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:47:28 2018

@author: buenov
"""

import json
import requests

# u = wind speed
# time = day or night
# cloud = 0-1 (% of the sky that is covered)
# Solar radiation = W/m2

def stabilityclass_APIday(u,cloud,altitude):
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
def stabilityclass_night(u,cloud):
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


def stabilityclass_API(city,country):
        # Gather weather parameters      time='day'
    url = 'https://api.ipgeolocation.io/astronomy?apiKey=00424bbd52cf442ea1e923480323e6c7&tz=%s/%s' % (country,city)
    res =requests.get(url,params={'q':'requests+language:python'})
    json_response = res.json()
    altitude = json_response['sun_altitude']
    urlw = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=3ba98f5e6c66ecde2678c62d5786143b' % city
    res2 =requests.get(urlw)
    json_response = res2.json()
    cloud = float(json_response['clouds']['all'])*0.01
    u = float(json_response['wind']['speed'])
    u = float(u) ; cloud=float(cloud) ; altitude=float(altitude)

    stabilityclasses={}
    stabilityclasses['Day']= stabilityclass_APIday(u,cloud,altitude)
    stabilityclasses['Night']= stabilityclass_night(u,cloud)
    return stabilityclasses,u

def stabilityclass_input(u,cloud,UV):
    u=float(u) ; cloud=float(cloud)
    stabilityclasses={}
    stabilityclasses['Day']= stabilityclass_inputday(u,cloud,UV)
    stabilityclasses['Night']= stabilityclass_night(u,cloud)
    return stabilityclasses
