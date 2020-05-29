#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:47:28 2018

@author: buenov
"""

import json
import requests


def RH_APIcall(lat,lon):
        # Gather weather parameters      time='day'
    apikey='a6a267d35d8c445bbc4f74dca9543661'
    url='https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key={}'.format(lat,lon,apikey)
    json_response = requests.get(url).json()
    content={}
    print(json_response)
    city=json_response['city_name']
    country=json_response['country_code']
    for day in enumerate(json_response["data"]):
        date=day[1]['valid_date']
        RH =day[1]['rh']
        precip=day[1]['precip']
        if (precip>0) or (RH >= 90): risk="High"
        if (precip==0) and RH >= 70 : risk="Medium"
        if (precip==0) and RH < 70 : risk="Low"
        content[date]=[RH,precip,risk]
    return (content, city, country)
