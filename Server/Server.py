#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import urllib

import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Server.models import resultAll, performanceData, listAPIMointor,CaseDetail


@csrf_exempt
def pushResults(request):
    api = 'server/result/push'
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
    print_Log(api, body_json)
    resultAll(Jenkinsid=body_json['data']['sum']['Jenkinsid'],sumery=body_json['data']['sum'],
              detail=body_json['data']['detail'],
              platform=body_json['data']['sum']['platform']).save()
    print_Log(api, '保存成功')
    return HttpResponse(simplejson.dumps(200))

@csrf_exempt
def pushMonitorResults(request):
    api = 'server/monitor/push'
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
    print_Log(api, body_json)
    listAPIMointor(rt=body_json['data']['rt'],only=body_json['data']['only'],
                   all=body_json['data']['allCaseNum'],
                   fail=body_json['data']['FailCaseName']).save()
    for item in body_json['data']['result']:
        CaseDetail(model=item['model'],api=item['api'],charger=item['charger'],caseName=item['caseName'],
                   result=item['res'],useTime=item['useTime'],comment=item['comment'],
                   all=item,only=body_json['data']['only']).save()
    print_Log(api, '保存成功')
    return HttpResponse(simplejson.dumps(200))

@csrf_exempt
def pushPerformanceData(request):
    api = 'server/pt/push'
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
    print_Log(api, body_json)
    performanceData(fps=body_json['data']['data']['fps'],cpu=body_json['data']['data']['cpu'],mem=body_json['data']['data']['mem'],
                    pageTime=body_json['data']['data']['pt'],startTime=body_json['data']['data']['st'],
                    Jenkinsid=body_json['data']['sum']['Jenkinsid'],Appname=body_json['data']['sum']['app'],
                    model=body_json['data']['sum']['model'],runt=body_json['data']['sum']['runt'],
                    CodeVersion=body_json['data']['sum']['codev'],
                    platform=body_json['data']['sum']['platform']).save()
    print_Log(api, '保存成功')
    return HttpResponse(simplejson.dumps(200))

def getRate(request):
    # 接口：server/result/rate
    # 方式：GET
    # 参数：platform = android or iOS
    api = 'server/result/rate'
    platform = request.GET.get('platform')
    print_Log(api, platform)
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
                list.append(100-detail['fail']/detail['all']*100)
            result['result'] = list
            result['code'] = 0
            print_Log(api, result)
            return (simplejson.dumps(result))
    else:
        result = {}
        object = resultAll.objects.filter(platform='android').order_by('-id')
        list = []
        for line in object[:7]:
            detail = eval(line.sumery)
            list.append(100 - detail['fail'] / detail['all'] * 100)
        result['android'] = list
        result['code'] = 0
        object = resultAll.objects.filter(platform='iOS').order_by('-id')
        list1 = []
        for line in object[:7]:
            detail = eval(line.sumery)
            list1.append(100 - detail['fail'] / detail['all'] * 100)
        result['ios'] = list1
        print_Log(api, result)
        return (simplejson.dumps(result))

def delResults(request):
    id = (request.GET.get('id'))
    ##print(id)
    object = resultAll.objects.filter(id=id)
    object.delete()
    return HttpResponse(simplejson.dumps(200))

def getResults(request):
    # 接口：server/result/get
    # 方式：GET
    # 参数：platform = android or iOS,jenkinsId=01
    api = 'server/result/get'
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    isHave = resultAll.objects.filter(Jenkinsid=id,platform=platform)
    result = {}
    if isHave:
        object = resultAll.objects.get(Jenkinsid=id,platform=platform)
        result['code'] = 0
        back = {}
        back['sum']=eval(object.sumery)
        back['detail'] = eval(object.detail)
        result['result']=back
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        result['code'] = -1
        result['result'] = {}
        print_Log(api, result)
        return simplejson.dumps(result)

def getPtResultsJson(request):
    api = 'server/pt/get'
    id = (request.GET.get('jenkinsId'))
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
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        result['code'] = -1
        result['result'] = {}
        print_Log(api, result)
        return simplejson.dumps(result)

def getResultslist(request):
    api = 'server/result/list'
    id = request.GET.get('platform')
    result ={}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    print_Log(api, id)
    if not object:
        result['code']=-1
        result['result']=[]
        print_Log(api, result)
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
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))

def getResultslistJson(request):
    api = 'server/result/listJson'
    id = request.GET.get('platform')
    print_Log(api, id)
    result ={}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        print_Log(api, result)
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
        print_Log(api, result)
        return simplejson.dumps(result)

def getPTResultslist(request):
    api = 'server/pt/list'
    id = request.GET.get('platform')
    print_Log(api, id)
    result ={}
    object = performanceData.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code']=-1
        result['result']=[]
        print_Log(api, result)
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
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))

def getPTResultslistJson(request):
    api = 'server/pt/list'
    id = request.GET.get('platform')
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

def getAPIMonitorDataJson(request):
    api = 'server/monitor/get'
    id = request.GET.get('only')
    print_Log(api, id)
    result = {}
    isHave = listAPIMointor.objects.filter(only=id)
    if not isHave:
        print('none')
        result['code'] = -1
        result['result'] = []
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        print('have')
        object = listAPIMointor.objects.get(only=id)
        Back = {}
        Back['rt'] = object.rt
        Back['code'] = 0
        Back['all'] = object.all
        Back['rate'] = object.fail/object.all*100
        failedlistCase = CaseDetail.objects.filter(only=id, result=-1)
        fail =[]
        for failitem in failedlistCase:
            item = {}
            item['model'] = failitem.model
            item['api'] = failitem.api
            item['charger'] = failitem.charger
            item['caseName'] = failitem.caseName
            item['useTime'] = failitem.useTime
            item['comment'] = failitem.comment
            fail.append(item)
        passlistCase = CaseDetail.objects.filter(only=id, result=0).order_by('-useTime')
        passlist = []
        for passitem in passlistCase:
            item = {}
            item['model'] = passitem.model
            item['api'] = passitem.api
            item['charger'] = passitem.charger
            item['caseName'] = passitem.caseName
            item['useTime'] = passitem.useTime
            item['comment'] = passitem.comment
            passlist.append(item)
        Back['faillist']=fail
        Back['passlist']=passlist
        print_Log(api, Back)
        return simplejson.dumps(Back)

def getAPIMonitorRateJson(request):
    api = 'server/monitor/list'
    object = listAPIMointor.objects.filter().order_by('-id')
    result = {}
    listrate=[]
    listall=[]
    if not object:
        result['code']=-1
        result['result']=[]
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        for item in object[:7]:
            back ={}
            back['rate'] = 100-item.fail/item.all*100
            back['only'] = item.only
            back['rt'] = item.rt
            listrate.append(100-item.fail/item.all*100)
            listall.append(back)
        result['code']=0
        result['result']=listall
        result['rate']=listrate
        print_Log(api, result)
        return simplejson.dumps(result)

def print_Log(api,context):
    # print('{0}--{1}-{2}'.format(currentTime(), api, context))
    fp = open('/work/log','a')
    fp.write('{0}--{1}-{2}'.format(currentTime(), api, context))
    fp.close()

def currentTime():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())