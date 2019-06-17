#!/usr/bin/env python3
# coding=UTF-8

# def testnew(request):
#     rrrr = Jobs.objects.all()
#     context = {'person': rrrr}
#     return render(request, 'TestNew.html', context)
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from Server import Server
from Server.models import resultAll

def index(request):
    t = get_template('index.html')
    html = t.render()
    return HttpResponse(html)

def getAndroidList(request):
    t = get_template('listAndroid.html')
    html = t.render()
    return HttpResponse(html)

def getiOSList(request):
    t = get_template('listiOS.html')
    html = t.render()
    return HttpResponse(html)

def Deatail(request):
    res = Server.getResults(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        print("fail")
        context = {'person': None}
    else:
        print('Pass')
        context = {'person': res_dict}
    print(context)
    return render(request, 'resultDetail.html', context)

def statistics(request):
    t = get_template('statistics.html')
    html = t.render()
    return HttpResponse(html)

def performanceListAndroid(request):
    t = get_template('performanceList.html')
    html = t.render()
    return HttpResponse(html)

def performanceListiOS(request):
    t = get_template('performanceListiOS.html')
    html = t.render()
    return HttpResponse(html)

def performance(request):
    res = Server.getPtResultsJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        print("fail")
        context = {'person': None}
    else:
        print('Pass')
        context = {'person': res_dict,'jss':res}
    print(context)
    return render(request, 'performance.html', context)