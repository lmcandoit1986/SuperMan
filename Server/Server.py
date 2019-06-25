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
    # 接口：server/result/push
    # 方式：POST
    # 参数：{ 'data':{
    #           'sum':{
    #                 'platform':'android or iOS',
    #                 'runt':'2019-07-01 12:10:01', 脚本触发的时间标示
    #                 'model':'HuaweiP9',设备型号
    #                 'uset':'',脚本执行耗时总长
    #                 'Jenkinsid':1, 唯一标示，用于获取测试结果
    #                 'app':'百度',测试App名称，统一即可，也可以写app Package 或 Boundid
    #                 'all':2,总用例数
    #                 'fail':1 失败用例数
    #                   },
    #             'detail':[
    #             {
    #               'caseName':'用例名称',
    #               'result':0 或者 -1，-1 为失败,
    #               'comment':'日志信息',
    #               'pic':'截图信息'
    #               },
    #             {
    #               'caseName':'用例名称',
    #               'result':0 或者 -1，-1 为失败,
    #               'comment':'日志信息',
    #               'pic':'截图信息'
    #               }
    #             ]
    #               }
    #       }
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))
    #print(body_json['data']['sum'])
    resultAll(Jenkinsid=body_json['data']['sum']['Jenkinsid'],sumery=body_json['data']['sum'],detail=body_json['data']['detail'],platform=body_json['data']['sum']['platform']).save()
    return HttpResponse(simplejson.dumps(200))

@csrf_exempt
def pushPerformanceData(request):
    # 接口：server/result/push
    # 方式：POST
    # 参数：{ 'data':
    #           'sum':{
    #               'Jenkinsid':1,
    #               'app':'百度',测试App名称，统一即可，也可以写app Package 或 Boundid
    #               'model':'HuaweiP9',设备型号
    #               'runt':'2019-07-01 12:10:01', 脚本触发的时间标示
    #               'codev':'123 代码code版本',
    #               'platform':'android or iOS'
    #               },
    #           'data':{'fps':
    #                       [
    #                           {'activity':'页面标识，最好为英文，会在结果页面展示',
    #                            'info':'页面简单信息介绍',
    #                            'data':[45,46,47,56,43,45,45]
    #                            },
    #                        ],
    #                   'mem':
    #                       [
    #                           {'activity':'页面标识，最好为英文，会在结果页面展示',
    #                            'info':'页面简单信息介绍',
    #                            'data':[45,46,47,56,43,45,45]
    #                            },
    #                       ],
    #                   'cpu':
    #                       [
    #                           {'activity':'',
    #                           'info':'',
    #                           'data':[23,12,41,32,12]
    #                           },
    #                       ],
    #                   'pt':
    #                       [
    #                           {'activity':'',
    #                            'info':'',
    #                            'data':460
    #                            },
    #                        ],
    #                   'st':
    #                       {
    #                           'sumer':123,
    #                           'data':[12,123,1234,12345]
    #                       }
    #           }
    #       }
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))
    #print(body_json['data']['sum'])
    performanceData(fps=body_json['data']['data']['fps'],cpu=body_json['data']['data']['cpu'],mem=body_json['data']['data']['mem'],pageTime=body_json['data']['data']['pt'],startTime=body_json['data']['data']['st'],Jenkinsid=body_json['data']['sum']['Jenkinsid'],Appname=body_json['data']['sum']['app'],model=body_json['data']['sum']['model'],runt=body_json['data']['sum']['runt'],CodeVersion=body_json['data']['sum']['codev'],platform=body_json['data']['sum']['platform']).save()
    return HttpResponse(simplejson.dumps(200))

def getRate(request):
    # 接口：server/result/rate
    # 方式：GET
    # 参数：platform = android or iOS
    platform = request.GET.get('platform')
    if not platform=='all':
        result = {}
        object = resultAll.objects.filter(platform=platform).order_by('-id')
        if not object:
            result['code'] = -1
            result['result'] = []
            return (simplejson.dumps(result))
        else:
            list = []
            for line in object[:7]:
                detail =eval(line.sumery)
                #print(detail)
                list.append(100-detail['fail']/detail['all']*100)
            result['result'] = list
            result['code'] = 0
            return (simplejson.dumps(result))
    else:
        result = {}
        object = resultAll.objects.filter(platform='android').order_by('-id')
        list = []
        for line in object[:7]:
            detail = eval(line.sumery)
            # print(detail)
            list.append(100 - detail['fail'] / detail['all'] * 100)
        result['android'] = list
        result['code'] = 0
        object = resultAll.objects.filter(platform='iOS').order_by('-id')
        list1 = []
        for line in object[:7]:
            detail = eval(line.sumery)
            # print(detail)
            list1.append(100 - detail['fail'] / detail['all'] * 100)
        result['ios'] = list1
        return (simplejson.dumps(result))


def delResults(request):
    id = (request.GET.get('id'))
    #print(id)
    object = resultAll.objects.filter(id=id)
    object.delete()
    return HttpResponse(simplejson.dumps(200))


def getResults(request):
    # 接口：server/result/get
    # 方式：GET
    # 参数：platform = android or iOS,jenkinsId=01
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    #print(id)
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
    #print(id)
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
    #print(id)
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

def getResultslistJson(request):
    id = request.GET.get('platform')
    #print(id)
    result ={}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        return simplejson.dumps(result)
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
        return simplejson.dumps(result)

def getPTResultslist(request):
    id = request.GET.get('platform')
    #print(id)
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

def getPTResultslistJson(request):
    id = request.GET.get('platform')
    #print(id)
    result ={}
    object = performanceData.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        return (simplejson.dumps(result))
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
        return (simplejson.dumps(result))