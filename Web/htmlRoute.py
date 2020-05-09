#!/usr/bin/env python3
# coding=UTF-8

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from Server import Server
from Server.models import Imgdb


def index(request):
    t = get_template('index.html')
    html = t.render()
    return HttpResponse(html)

def sms(request):
    t = get_template('SMS.html')
    html = t.render()
    return HttpResponse(html)

def new(request):
    t = get_template('mock.html')
    html = t.render()
    return HttpResponse(html)

def error(request):
    # conten = {'person':""}
    t = get_template('error.html')
    html = t.render()
    return HttpResponse(html)

def mocklist(request):
    res = Server.mock_data_list(request)
    res_dict = eval(res)
    context = {'person': res_dict}
    return render(request, 'mockList.html', context)

def uiauto(request):
    res = Server.getListResultNew(request)
    res_dict = eval(res)
    print(res_dict)
    context = {'person': res, 'dict_data': res_dict}
    return render(request, 'base.html', context)
    # t = get_template('base.html')
    # html = t.render()
    # return HttpResponse(html)

def APIWatcher(request):
    res = Server.getAPIMonitorDataJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res,'dict_data':res_dict}
    # print(context)
    return render(request,'CheckAPI.html',context)

def getAndroidList(request):
    res = Server.getResultslistJson(request)
    res_dict = eval(res)
    res2 =Server.getRate(request)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict,'rate':res2}
    print(context)
    return render(request, 'listAndroid.html', context)

def getAPIMonitorList(request):
    res = Server.getAPIMonitorRateJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res,'JS':res_dict}
    # print(context)
    return render(request, 'listAPIMonitor.html', context)

def getiOSList(request):
    res = Server.getResultslistJson(request)
    res_dict = eval(res)
    res2 = Server.getRate(request)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict, 'rate': res2}
    # print(context)
    return render(request, 'listiOS.html', context)

def Deatail(request):
    res = Server.getResults(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict}
    # print(context)
    return render(request, 'resultDetail.html', context)

def Deatailv2(request):
    res = Server.getResultsv2(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict}
    print(context)
    return render(request, 'resultDetailv2.html', context)

def Deatailv3(request):
    key = 0
    if request.GET['user'] == 'visitor':
        key = 0
    elif request.GET['user'] == 'admin':
        key = 1
    res = Server.getResultsv3(request)
    res_dict = eval(res)
    res2 = Server.getRealReason(request)
    res2_dict = eval(res2)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict,'reason':res2_dict,'key':key}
    print(context)
    return render(request, 'resultDetailNew.html', context)

def statistics(request):
    res = Server.getRate(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'personjson': None}
    else:
        # print('Pass')
        context = {'personjson':res}
    # print(context)
    return render(request, 'statistics.html', context)

def performanceListAndroid(request):
    res = Server.getPTResultslistJson(request)
    res_dict =eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        print('Pass')
        context = {'person':res_dict}
    print(context)
    return render(request, 'performanceList.html', context)


def performanceListiOS(request):
    res = Server.getPTResultslistJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict}
    print(context)
    return render(request, 'performanceListiOS.html', context)

def performanceList(request):
    res = Server.getPTResultslistJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict}
    # print(context)
    return render(request, 'performanceListNew.html', context)

def performance(request):
    res = Server.getPtResultsJson(request)
    res_dict = eval(res)
    if res_dict['code'] == -1:
        # print("fail")
        context = {'person': None}
    else:
        # print('Pass')
        context = {'person': res_dict,'jss':res}
    print(context)
    return render(request, 'performance.html', context)