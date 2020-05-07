#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import urllib

import requests
import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Server.models import resultAll, performanceData, listAPIMointor, CaseDetail, UICaseDetail, uiAutoRunListN, \
    mockData, failReason


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
    objects = resultAll.objects.filter(Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                                       platform=body_json['data']['sum']['platform'])
    if objects:
        result = {}
        result['code'] = 100
        result['msg'] = '数据库已存在该jenkinsid,请检查后重试'
        return HttpResponse(simplejson.dumps(result))
    else:
        if body_json['data']['detail']:
            resultAll(Jenkinsid=body_json['data']['sum']['Jenkinsid'], sumery=body_json['data']['sum'],
                      detail=body_json['data']['detail'],
                      platform=body_json['data']['sum']['platform']).save()
            object = resultAll.objects.get(Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                                           platform=body_json['data']['sum']['platform'])
            print_Log(api, '保存成功')
            result = {}
            result['code'] = 0
            result['msg'] = 'id={0}'.format(object.id)
            return HttpResponse(simplejson.dumps(result))
        else:
            result = {}
            result['code'] = 101
            result['msg'] = '用例为空'
            return HttpResponse(simplejson.dumps(result))


@csrf_exempt
def pushResultsV2(request):
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
    objects = resultAll.objects.filter(Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                                       platform=body_json['data']['sum']['platform'])
    if objects:
        result = {}
        result['code'] = 100
        result['msg'] = '数据库已存在该jenkinsid,请检查后重试'
        return HttpResponse(simplejson.dumps(result))
    else:
        if body_json['data']['detail']:
            resultAll(Jenkinsid=body_json['data']['sum']['Jenkinsid'], sumery=body_json['data']['sum'],
                      detail=body_json['data']['detail'],
                      platform=body_json['data']['sum']['platform']).save()
            # object = resultAll.objects.get(Jenkinsid=body_json['data']['sum']['Jenkinsid'],platform=body_json['data']['sum']['platform'])
            for item in body_json['data']['detail']:
                UICaseDetail(model=item['model'], case=item['case'], caseName=item['caseName'], result=item['result'],
                             useTime=item['useTime'], comment=item['comment'], pic=item['pic'], listid=0,
                             platform=body_json['data']['sum']['platform'],
                             Jenkinsid=body_json['data']['sum']['Jenkinsid'], all=item, reason=0).save()
            print_Log(api, '保存成功')
            result = {}
            result['code'] = 0
            result['msg'] = 'id'
            return HttpResponse(simplejson.dumps(result))
        else:
            result = {}
            result['code'] = 101
            result['msg'] = '用例为空'
            return HttpResponse(simplejson.dumps(result))


@csrf_exempt
def pushResultsV3(request):
    api = 'server/result/pushV3'
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))
    print(api, body_json)
    objects = uiAutoRunListN.objects.filter(Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                                            platform=body_json['data']['sum']['platform'])
    # print(objects.id)
    if objects:
        result = {}
        result['code'] = 100
        result['msg'] = '数据库已存在该jenkinsid,请检查后重试'
        return HttpResponse(simplejson.dumps(result))
    else:
        # sum['platform'] = 'iOS'
        # sum['app'] = '平安健康险'
        # sum['model'] = Config.devices
        # sum['module'] = self.getModelList(item)
        # sum['uset'] = '{0} m'.format(round(self.getAlltime(item) / 60, 2))
        # sum['runt'] = time.strftime("%Y-%m-%d %X", time.localtime())
        # sum['all'] = len(item)
        # sum['version'] = '3.13s.1'
        # sum['fail'] = self.getFailed(item)
        # sum['Jenkinsid'] = time.strftime("%Y%m%d%H%M", time.localtime())
        if body_json['data']['sum']['all']:
            uiAutoRunListN(platform=body_json['data']['sum']['platform'], allNum=body_json['data']['sum']['all'],
                           failNum=body_json['data']['sum']['fail'], rt=body_json['data']['sum']['runt'],
                           ut=body_json['data']['sum']['uset'], Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                           link='', appName=body_json['data']['sum']['app'], model='',
                           device=body_json['data']['sum']['model'], appVersion=body_json['data']['sum']['version']).save()

            for item in body_json['data']['detail']:
                UICaseDetail(model=item['model'], case=item['case'], caseName=item['caseName'], result=item['result'],
                             useTime=item['useTime'],
                             comment=item['comment'], pic=item['pic'], listid=0,
                             platform=body_json['data']['sum']['platform'], Jenkinsid=body_json['data']['sum']['Jenkinsid'],
                             all=item, reason=0).save()
        print_Log(api, '保存成功')
        result = {}
        result['code'] = 0
        result['msg'] = ''
        return HttpResponse(simplejson.dumps(result))


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
    listAPIMointor(rt=body_json['data']['rt'], only=body_json['data']['only'],
                   all=body_json['data']['allCaseNum'],
                   fail=body_json['data']['FailCaseName']).save()
    for item in body_json['data']['result']:
        CaseDetail(model=item['model'], api=item['api'], charger=item['charger'], caseName=item['caseName'],
                   result=item['res'], useTime=item['useTime'], comment=item['comment'],
                   all=item, only=body_json['data']['only']).save()
    # print_Log(api, '保存成功')
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
    #               'platform':'Android or iOS'
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
    performanceData(fps=body_json['data']['data']['fps'], cpu=body_json['data']['data']['cpu'],
                    mem=body_json['data']['data']['mem'],
                    pageTime=body_json['data']['data']['pt'], startTime=body_json['data']['data']['st'],
                    Jenkinsid=body_json['data']['sum']['Jenkinsid'], Appname=body_json['data']['sum']['app'],
                    model=body_json['data']['sum']['model'], runt=body_json['data']['sum']['runt'],
                    CodeVersion=body_json['data']['sum']['codev'],
                    platform=body_json['data']['sum']['platform']).save()
    print_Log(api, '保存成功')
    return HttpResponse(simplejson.dumps(200))


def getRate(request):
    # 接口：server/result/rate
    # 方式：GET
    # 参数：platform = Android or iOS
    api = 'server/result/rate'
    platform = request.GET.get('platform')
    print_Log(api, platform)
    if not platform == 'all':
        result = {}
        object = resultAll.objects.filter(platform=platform).order_by('-id')
        if not object:
            result['code'] = -1
            result['result'] = []
            return (simplejson.dumps(result))
        else:
            list = []
            for line in object[:7]:
                detail = eval(line.sumery)
                list.append(100 - detail['fail'] * 100 // detail['all'])
            result['result'] = list
            result['code'] = 0
            print_Log(api, result)
            return (simplejson.dumps(result))
    else:
        result = {}
        object = resultAll.objects.filter(platform='Android').order_by('-id')
        list = []
        for line in object[:7]:
            detail = eval(line.sumery)
            list.append(100 - detail['fail'] * 100 // detail['all'])
        result['android'] = list
        result['code'] = 0
        object = resultAll.objects.filter(platform='iOS').order_by('-id')
        list1 = []
        for line in object[:7]:
            detail = eval(line.sumery)
            list1.append(100 - detail['fail'] * 100 // detail['all'])
        result['ios'] = list1
        print_Log(api, result)
        return (simplejson.dumps(result))


def delResults(request):
    id = (request.GET.get('id'))
    ##print(id)
    object = resultAll.objects.filter(id=id)
    object.delete()
    return HttpResponse(simplejson.dumps(200))


@csrf_exempt
def getListResultNew(request):
    objectAndroid = uiAutoRunListN.objects.filter(platform='Android').order_by('-id')
    objectiOS = uiAutoRunListN.objects.filter(platform='iOS').order_by('-id')
    Rate = {}
    Result = {}
    if objectAndroid:
        androidRateList = []
        for item in objectAndroid[:7]:
            if item:
                androidRateList.append(100 - item.failNum * 100 // item.allNum)
            else:
                androidRateList.append(0)
        Rate['android'] = androidRateList
    if objectiOS:
        iOSRateList = []
        for item in objectiOS[:7]:
            if item:
                iOSRateList.append(100 - item.failNum * 100 // item.allNum)
            else:
                iOSRateList.append(0)
        Rate['ios'] = iOSRateList
    Result['rate'] = Rate
    objectAll = uiAutoRunListN.objects.all().order_by('-id')
    if objectAll:
        listAll = []
        for item in objectAll[:14]:
            if item:
                itemdic = {}
                itemdic['allNum'] = item.allNum
                itemdic['id'] = item.id
                itemdic['failNum'] = item.failNum
                itemdic['device'] = item.device
                itemdic['appVersion'] = item.appVersion
                itemdic['Jenkinsid'] = item.Jenkinsid
                itemdic['appName'] = item.appName
                itemdic['ut'] = item.ut
                itemdic['rt'] = item.rt
                itemdic['platform'] = item.platform
                itemdic['model'] = item.model
                itemdic['link'] = item.link
                listAll.append(itemdic)
        Result['list'] = listAll
    header = {}
    header["Access-Control-Allow-Origin"] = "http://192.168.199.139"
    # return HttpResponse(simplejson.dumps(Result),headers=header)
    return simplejson.dumps(Result)


def getResults(request):
    # 接口：server/result/get
    # 方式：GET
    # 参数：platform = android or iOS,jenkinsId=01
    api = 'server/result/get'
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    isHave = resultAll.objects.filter(Jenkinsid=id, platform=platform)
    result = {}
    if isHave:
        object = resultAll.objects.get(Jenkinsid=id, platform=platform)
        result['code'] = 0
        result['id'] = object.id
        back = {}
        back['sum'] = eval(object.sumery)
        back['detail'] = eval(object.detail)
        result['result'] = back
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        result['code'] = -1
        result['result'] = {}
        print_Log(api, result)
        return simplejson.dumps(result)


def getResultsv3(request):
    # 接口：server/result/get
    # 方式：GET
    # 参数：platform = android or iOS,jenkinsId=01
    api = 'server/result/get'
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    isHave = uiAutoRunListN.objects.filter(Jenkinsid=id, platform=platform)
    result = {}
    if isHave:
        object = uiAutoRunListN.objects.get(Jenkinsid=id, platform=platform)
        result['code'] = 0
        result['id'] = object.id
        itemdic = {}
        itemdic['allNum'] = object.allNum
        itemdic['id'] = object.id
        itemdic['failNum'] = object.failNum
        itemdic['device'] = object.device
        itemdic['appVersion'] = object.appVersion
        itemdic['Jenkinsid'] = object.Jenkinsid
        itemdic['appName'] = object.appName
        itemdic['ut'] = object.ut
        itemdic['rt'] = object.rt
        itemdic['platform'] = object.platform
        itemdic['rate'] = 100 - object.failNum * 100 // object.allNum
        itemdic['model'] = object.model
        itemdic['link'] = object.link
        result['sum'] = itemdic
        listCase = UICaseDetail.objects.filter(platform=platform, Jenkinsid=id)
        list = []
        reasons = []
        backNum = []
        backReason = []
        for case in listCase:
            casedetail = {}
            casedetail['id'] = case.id
            casedetail['model'] = case.model
            casedetail['case'] = case.case
            casedetail['caseName'] = case.caseName
            casedetail['result'] = case.result
            casedetail['useTime'] = case.useTime
            casedetail['comment'] = case.comment
            casedetail['reason'] = case.reason
            if case.result != 0:
                reasons.append(case.reason)
            if case.pic != '':
                casedetail['pic'] = 'img/' + case.pic
            else:
                casedetail['pic'] = case.pic
            list.append(casedetail)
        list.sort(key=takeRes, reverse=True)
        print(reasons)
        for line in set(reasons):
            backReason.append((failReason.objects.get(id=line).reason))
            backNum.append(reasons.count(line))
        # print(back)
        result['rN'] = backNum
        result['rD'] = backReason
        result['detail'] = list

        return simplejson.dumps(result)

    else:
        result['code'] = -1
        result['result'] = {}
        print_Log(api, result)
        return simplejson.dumps(result)

def takeRes(el):
    return el['result']


def getResultsv2(request):
    # 接口：server/result/get
    # 方式：GET
    # 参数：platform = android or iOS,jenkinsId=01
    api = 'server/result/get'
    id = (request.GET.get('jenkinsId'))
    platform = request.GET.get('platform')
    isHave = resultAll.objects.filter(Jenkinsid=id, platform=platform)
    result = {}
    if isHave:
        object = resultAll.objects.get(Jenkinsid=id, platform=platform)
        result['code'] = 0
        result['id'] = object.id
        back = {}
        back['sum'] = eval(object.sumery)
        detail = []
        print('id:{}'.format(object.id))
        for model in back['sum']['module']:
            item = {}
            item['model'] = model
            failedlist = UICaseDetail.objects.filter(Jenkinsid=id, platform=platform, model=model, result=-1)
            listf = []
            for line in failedlist:
                item1 = {}
                item1['case'] = line.case
                item1['caseName'] = line.caseName
                item1['useTime'] = line.useTime
                item1['comment'] = line.comment
                item1['pic'] = line.pic
                listf.append(item1)

            item['failed'] = listf
            passlist = UICaseDetail.objects.filter(Jenkinsid=id, platform=platform, model=model, result=0)
            listp = []
            for linep in passlist:
                item1 = {}
                item1['case'] = linep.case
                item1['caseName'] = linep.caseName
                item1['useTime'] = linep.useTime
                item1['comment'] = linep.comment
                item1['pic'] = linep.pic
                print(item1)
                listp.append(item1)
            item['pass'] = listp

            SElist = UICaseDetail.objects.filter(Jenkinsid=id, platform=platform, model=model, result=-2)
            listp = []
            for linep in SElist:
                item1 = {}
                item1['case'] = linep.case
                item1['caseName'] = linep.caseName
                item1['useTime'] = linep.useTime
                item1['comment'] = linep.comment
                item1['pic'] = linep.pic
                print(item1)
                listp.append(item1)
            item['ServerError'] = listp

            EXlist = UICaseDetail.objects.filter(Jenkinsid=id, platform=platform, model=model, result=-3)
            listp = []
            for linep in EXlist:
                item1 = {}
                item1['case'] = linep.case
                item1['caseName'] = linep.caseName
                item1['useTime'] = linep.useTime
                item1['comment'] = linep.comment
                item1['pic'] = linep.pic
                print(item1)
                listp.append(item1)
            item['EX'] = listp

            detail.append(item)

        back['detail'] = detail
        result['result'] = back
        result['rate'] = back['sum']['fail'] * 100 // back['sum']['all']
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
        result['id'] = object.id
        back = {}
        back['platform'] = object.platform
        back['jenkinsId'] = id
        back['app'] = object.Appname
        back['codeversion'] = object.CodeVersion
        back['st'] = eval(object.startTime)
        back['pt'] = eval(object.pageTime)
        back['fps'] = eval(object.fps)
        back['cpu'] = eval(object.cpu)
        back['mem'] = eval(object.mem)
        back['rt'] = object.runt
        result['result'] = back
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
    result = {}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    print_Log(api, id)
    if not object:
        result['code'] = -1
        result['result'] = []
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))
    else:
        Back = {}
        list = []
        for line in object[:7]:
            item = {}
            item['sum'] = eval(line.sumery)
            list.append(item)
        Back['all'] = list
        result['result'] = list
        result['code'] = 0
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))


def getResultslistJson(request):
    api = 'server/result/listJson'
    id = request.GET.get('platform')
    print_Log(api, id)
    result = {}
    object = resultAll.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code'] = -1
        result['result'] = []
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        Back = {}
        list = []
        for line in object[:7]:
            item = {}
            item['id'] = line.id
            item['sum'] = eval(line.sumery)
            list.append(item)
        Back['all'] = list
        result['result'] = list
        result['code'] = 0

        print_Log(api, result)
        return simplejson.dumps(result)


def getPTResultslist(request):
    api = 'server/pt/list'
    id = request.GET.get('platform')
    print_Log(api, id)
    result = {}
    object = performanceData.objects.filter(platform=id).order_by('-id')
    if not object:
        result['code'] = -1
        result['result'] = []
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))
    else:
        Back = {}
        list = []
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
        Back['all'] = list
        result['result'] = list
        result['code'] = 0
        print_Log(api, result)
        return HttpResponse(simplejson.dumps(result))


def getPTResultslistJson(request):
    api = 'server/pt/list'
    id = request.GET.get('platform')
    result = {}
    if id == 'all':
        object = performanceData.objects.all().order_by('-id')
        if not object:
            result['code'] = -1
            result['result'] = []
            return (simplejson.dumps(result))
        else:
            Back = {}
            list = []
            for line in object[:14]:
                back = {}
                back['platform'] = line.platform
                back['id'] = line.id
                back['Jenkinsid'] = line.Jenkinsid
                back['app'] = line.Appname
                back['model'] = line.model
                back['codeversion'] = line.CodeVersion
                back['rt'] = line.runt
                result['result'] = back
                list.append(back)
            Back['all'] = list
            result['result'] = list
            result['code'] = 0
            return (simplejson.dumps(result))
    else:
        object = performanceData.objects.filter(platform=id).order_by('-id')
        if not object:
            result['code'] = -1
            result['result'] = []
            return (simplejson.dumps(result))
        else:
            Back = {}
            list = []
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
            Back['all'] = list
            result['result'] = list
            result['code'] = 0
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
        Back['id'] = object.id
        Back['code'] = 0
        Back['all'] = object.all
        Back['rate'] = object.fail * 100 // object.all
        failedlistCase = CaseDetail.objects.filter(only=id, result=-1)
        fail = []
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
        Back['faillist'] = fail
        Back['passlist'] = passlist
        print_Log(api, Back)
        return simplejson.dumps(Back)


def getAPIMonitorRateJson(request):
    api = 'server/monitor/list'
    object = listAPIMointor.objects.filter().order_by('-id')
    result = {}
    listrate = []
    listall = []
    if not object:
        result['code'] = -1
        result['result'] = []
        print_Log(api, result)
        return simplejson.dumps(result)
    else:
        for item in object[:7]:
            back = {}
            back['rate'] = 100 - item.fail * 100 // item.all
            back['only'] = item.only
            back['rt'] = item.rt
            listrate.append(100 - item.fail * 100 // item.all)
            listall.append(back)
        result['code'] = 0
        result['result'] = listall
        result['rate'] = listrate
        print_Log(api, result)
        return simplejson.dumps(result)


def print_Log(api, context):
    # print('{0}--{1}-{2}'.format(currentTime(), api, context))
    fp = open('/work/log', 'a')
    fp.write('{0}--{1}-{2}'.format(currentTime(), api, context))
    fp.close()


def currentTime():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


@csrf_exempt
def mock_data_insert(request):
    api = request.POST['api']
    jsonData = request.POST['jsonData']
    key = request.POST['key']
    if request.POST:
        if api == '' or jsonData == '' or key == '':
            context = {'person': "api or json data 数据为空"}
            return render(request, 'error.html', context)
        try:
            dictData = eval(request.POST['jsonData'])
        except NameError as ne:
            context = {'person': "json data 数据格式异常"}
            return render(request, 'error.html', context)
        except SyntaxError as se:
            context = {'person': "json data 数据格式异常"}
            return render(request, 'error.html', context)

    item = mockData.objects.filter(api=api)
    if item:
        context = {'person': "api 数据重复"}
        return render(request, 'error.html', context)
        # return HttpResponse(simplejson.dumps({'code': -1, 'msg': '数据重复'}))
    else:
        mockData(api=api, data=dictData, keyword=key, status=0).save()
        return render(request, 'mock.html')


def getRealReason(request):
    if request.GET:
        items = failReason.objects.all()
        res = []
        for item in items:
            itemDict = {}
            itemDict['id'] = item.id
            itemDict['reason'] = item.reason
            res.append(itemDict)
        return simplejson.dumps(res)


def setRealReason(request):
    if request.GET:
        caseid = request.GET['caseid']
        reasonid = request.GET['reasonid']
        item = UICaseDetail.objects.get(id=caseid)
        item.reason = reasonid
        item.save()
        return HttpResponse(200)


def mock_data_list(request):
    all = mockData.objects.all().order_by('-id')
    result = []
    for item in all:
        itemdict = {}
        itemdict['id'] = item.id
        itemdict['api'] = item.api
        itemdict['status'] = item.status
        itemdict['key'] = item.keyword
        itemdict['data'] = eval(item.data)
        result.append(itemdict)
    return simplejson.dumps(result)


def mock_data_del(request):
    if request.GET:
        id = request.GET['id']
        print(id)
        item = mockData.objects.get(id=id)
        item.delete()
        res = mock_data_list(request)
        res_dict = eval(res)
        context = {'person': res_dict}
        return render(request, 'mockList.html', context)


def mock_data_status_change(request):
    if request.GET:
        id = request.GET['id']
        status = request.GET['status']
        item = mockData.objects.get(id=id)
        item.status = status
        item.save()
        return HttpResponse(200)


def mock_data_edit(request):
    if request.POST:
        id = request.POST['id']
        try:
            status = eval(request.POST['jsonData'])
            item = mockData.objects.get(id=id)
            item.data = status
            item.save()
        except NameError as ne:
            context = {'person': "json data 数据格式异常"}
            return render(request, 'error.html', context)
        except SyntaxError as se:
            context = {'person': "json data 数据格式异常"}
            return render(request, 'error.html', context)
        res = mock_data_list(request)
        res_dict = eval(res)
        context = {'person': res_dict}
        return render(request, 'mockList.html', context)


def mock_data_get_by_api(request):
    if request.GET:
        key = request.GET['key']
        print(key)
        items = mockData.objects.filter(api=key)
        if items:
            result = []
            for item in items:
                itemdict = {}
                itemdict['id'] = item.id
                itemdict['key'] = item.keyword
                itemdict['api'] = item.api
                itemdict['status'] = item.status
                itemdict['data'] = eval(item.data)
                result.append(itemdict)
            context = {'person': result}
            return render(request, 'mockList.html', context)
            # return HttpResponse(simplejson.dumps(result))
        context = {'person': None}
        return render(request, 'mockList.html', context)
        # return HttpResponse(simplejson.dumps([]))

def mock_data_get_by_id(request):
    if request.GET:
        id = request.GET['id']
        objects = mockData.objects.filter(id=id)
        if objects:
            return HttpResponse(simplejson.dumps(eval(objects[0].data)))
        else:
            itemdict = {}
            itemdict['code'] = -1
            itemdict['msg'] = '无匹配数据或数据停用状态'
            return HttpResponse(simplejson.dumps(itemdict))

def mock_data_get_by_api_key(request):
    if request.GET:
        api = request.GET['api']
        key = request.GET['key']
        objects = mockData.objects.filter(api=api, status=0, keyword=key)
        if objects:
            return HttpResponse(simplejson.dumps(eval(objects[0].data)))
        else:
            itemdict = {}
            itemdict['code'] = -1
            itemdict['msg'] = '无匹配数据或数据停用状态'
            return HttpResponse(simplejson.dumps(itemdict))

def investMSBank(request):
    if request.GET:
        user = request.GET['user']
        psw = request.GET['psw']
        money = request.GET['money']
        cookies = requests.post(url='http://10.211.4.111/api2/auth/login',
                                json={"username": user, "password": psw}).cookies.get_dict()
        print(cookies)
        headers = {'User-Agent': 'HN-Salary Android/6.7.2.772.772 (9; HUAWEI;EML-AL00) 2159x1080 [qh360]',
                   'Content-Type': 'application/json'}

        res = requests.post(url='http://10.211.4.111:8891/api/v3/bankplus/cmbc/ebank-transfer/transfer-in',
                            json={"applicationAmount": money},
                            headers=headers,
                            cookies=cookies).json()
        print(res)
        return HttpResponse(200)
