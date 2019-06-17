#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib

import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Server.models import resultAll, performanceData


@csrf_exempt
def pushResults(request):
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))
    print(body_json['data']['sum'])
    resultAll(Jenkinsid=body_json['data']['sum']['Jenkinsid'],sumery=body_json['data']['sum'],detail=body_json['data']['detail'],platform=body_json['data']['sum']['platform']).save()
    return HttpResponse(simplejson.dumps(200))

@csrf_exempt
def pushPerformanceData(request):
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))
    print(body_json['data']['sum'])
    performanceData(fps=body_json['data']['data']['fps'],cpu=body_json['data']['data']['cpu'],mem=body_json['data']['data']['mem'],pageTime=body_json['data']['data']['pt'],startTime=body_json['data']['data']['st'],Jenkinsid=body_json['data']['sum']['Jenkinsid'],Appname=body_json['data']['sum']['app'],model=body_json['data']['sum']['model'],runt=body_json['data']['sum']['runt'],CodeVersion=body_json['data']['sum']['codev'],platform=body_json['data']['sum']['platform']).save()
    return HttpResponse(simplejson.dumps(200))

def getRate(request):
    platform = request.GET.get('platform')
    print(platform)
    result = {}
    object = resultAll.objects.filter(platform=platform).order_by('-id')
    if not object:
        result['code'] = -1
        result['result'] = []
        return HttpResponse(simplejson.dumps(result))
    else:
        list = []
        for line in object[:7]:
            detail =eval(line.sumery)
            print(detail)
            list.append(100-detail['fail']/detail['all']*100)
        result['result'] = list
        result['code'] = 0
        return HttpResponse(simplejson.dumps(result))

def delResults(request):
    id = (request.GET.get('id'))
    print(id)
    object = resultAll.objects.filter(id=id)
    object.delete()
    return HttpResponse(simplejson.dumps(200))


def getResults(request):
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    print(id)
    isHave = resultAll.objects.filter(Jenkinsid=id,platform=platform)
    result = {}
    if isHave:
        object = resultAll.objects.get(Jenkinsid=id,platform=platform)
        result['code'] = 0
        back = {}
        back['sum']=eval(object.sumery)
        back['detail'] = eval(object.detail)
        result['result']=back
        return simplejson.dumps(result)
    else:
        result['code'] = -1
        result['result'] = {}
        return simplejson.dumps(result)

def getPtResultsJson(request):
    id = (request.GET.get('jenkinsId'))
    print(id)
    isHave = performanceData.objects.filter(Jenkinsid=id)
    result = {}
    if isHave:
        object = performanceData.objects.get(Jenkinsid=id)
        result['code'] = 0
        back = {}
        back['platform']=object.platform
        back['jenkinsId'] = id
        back['app']=object.Appname
        back['codeversion']=object.CodeVersion
        back['st']=eval(object.startTime)
        back['pt']=eval(object.pageTime)
        back['fps']=eval(object.fps)
        back['cpu'] = eval(object.cpu)
        back['mem'] = eval(object.mem)
        back['rt'] =object.runt
        result['result']=back
        return simplejson.dumps(result)
    else:
        result['code'] = -1
        result['result'] = {}
        return simplejson.dumps(result)


def getResultslist(request):
    id = request.GET.get('platform')
    print(id)
    result ={}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        return HttpResponse(simplejson.dumps(result))
    else:
        Back ={}
        list =[]
        for line in object[:7]:
            item ={}
            item['sum']=eval(line.sumery)
            list.append(item)
        Back['all']=list
        result['result']=list
        result['code']=0
        return HttpResponse(simplejson.dumps(result))

def getPTResultslist(request):
    id = request.GET.get('platform')
    print(id)
    result ={}
    object = performanceData.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        return HttpResponse(simplejson.dumps(result))
    else:
        Back ={}
        list =[]
        for line in object[:7]:
            back = {}
            back['platform'] = line.platform
            back['Jenkinsid'] = line.Jenkinsid
            back['app'] = line.Appname
            back['model'] = line.model
            back['codeversion'] = line.CodeVersion
            back['rt'] = line.runt
            result['result'] = back
            list.append(back)
        Back['all']=list
        result['result']=list
        result['code']=0
        return HttpResponse(simplejson.dumps(result))