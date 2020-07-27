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

from Server import ModelObject
from Server.models import resultAll, performanceData, listAPIMointor, Imgdb
from Server.models import CaseDetail, UICaseDetail, uiAutoRunListN
from Server.models import mockData, failReason, APIrunlist, apiCases


@csrf_exempt
def api_auto_detail_del(request):
    if request.GET:
        id = request.GET['id']
    else:
        return HttpResponse(simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'}))

    item = uiAutoRunListN.objects.get(id=id)
    item.delete()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': 'pass'}))


@csrf_exempt
def api_auto_detail(request):
    if request.POST:
        platform = request.POST['platform']
        id = request.POST['jenkinsId']
    elif request.GET:
        platform = request.GET['platform']
        id = request.GET['jenkinsId']
    else:
        return simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'})

    '''
    先验证数据库是否有匹配数据
    '''
    if not assertUiAutoRunListObjectIsExist(id, platform):
        return simplejson.dumps({'code': -2, 'msg': '数据库无匹配数据'})

    result = {}  # 返回对象
    '''
    sum信息汇总
    '''
    sumOb = uiAutoRunListN.objects.get(Jenkinsid=id, platform=platform)
    result['sum'] = ModelObject.objectUiAutoRunList(sumOb)

    '''
    用例明细
    '''
    result['detail'] = []
    reasons = []
    listCase = UICaseDetail.objects.filter(platform=platform, Jenkinsid=id)
    for case in listCase:
        result['detail'].append(ModelObject.objectUICaseDetail(case))
        if case.result != 0:
            if case.reason == 0:
                reasons.append(1)
            else:
                reasons.append(case.reason)

    result['detail'].sort(key=takeRes, reverse=True)
    '''
    失败原因
    '''
    result['rD'] = []
    result['rN'] = []
    change = False
    for line in set(reasons):
        if line == 0:
            line = 1
            change = True
        res = failReason.objects.get(id=line)
        if res:
            result['rD'].append(res.reason)
            if change:
                result['rN'].append(reasons.count(line - 1))
            else:
                result['rN'].append(reasons.count(line))
        else:
            result['rD'].append('未定位')
            result['rN'].append(1)

    result['code'] = 0
    result['msg'] = '成功'

    return simplejson.dumps(result)


@csrf_exempt
def api_auto_list(request):
    objectAndroid = uiAutoRunListN.objects.filter(platform='Android').order_by('-id')[0:30]
    objectiOS = uiAutoRunListN.objects.filter(platform='iOS').order_by('-id')[0:7]

    Result = {
        'Android': {},
        'iOS': {}
    }

    if objectAndroid:
        Result['Android']['rate'] = []
        Result['Android']['list'] = []
        for item in objectAndroid:
            if item.allNum == 0:
                Result['Android']['rate'].append(0)
            else:
                Result['Android']['rate'].append(100 - item.failNum * 100 // item.allNum)
            Result['Android']['list'].append(ModelObject.objectUiAutoRunList(item))
    if objectiOS:
        Result['iOS']['rate'] = []
        Result['iOS']['list'] = []
        for item in objectiOS:
            if item.allNum != 0:
                Result['iOS']['rate'].append(100 - item.failNum * 100 // item.allNum)
            else:
                Result['iOS']['rate'].append(0)
            Result['iOS']['list'].append(ModelObject.objectUiAutoRunList(item))

    Result['code'] = 0
    Result['msg'] = '成功'

    return simplejson.dumps(Result)


@csrf_exempt
def api_auto_result_upload(request):
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))

    sum = body_json['data']['sum']
    if assertUiAutoRunListObjectIsExist(sum['Jenkinsid'], sum['platform']):
        return HttpResponse(simplejson.dumps({'code': -2, 'msg': '数据库已存在匹配数据'}))

    uiAutoRunListN(platform=sum['platform'],
                   allNum=sum['all'],
                   failNum=sum['fail'],
                   rt=sum['runt'],
                   ut=sum['uset'],
                   Jenkinsid=sum['Jenkinsid'],
                   link='',
                   appName=sum['app'],
                   model='',
                   device=sum['model'],
                   appVersion=sum['version']) \
        .save()

    for item in body_json['data']['detail']:
        UICaseDetail(model=getValue(item, 'model'),
                     case=getValue(item, 'case'),
                     caseName=getValue(item, 'caseName'),
                     result=getValue(item, 'result'),
                     useTime=getValue(item, 'useTime'),
                     comment=getValue(item, 'comment'),
                     pic=getValue(item, 'pic'),
                     listid=0,
                     platform=sum['platform'],
                     Jenkinsid=sum['Jenkinsid'],
                     all=item,
                     reason=0) \
            .save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))


@csrf_exempt
def api_mock_data_edit(request):
    if request.POST:
        id = request.POST['id']
        key = request.POST['key']
        value = request.POST['value']
    elif request.GET:
        id = request.GET['id']
        key = request.GET['key']
        value = request.GET['value']
    else:
        return simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'})

    item = mockData.objects.get(id=id)
    if key == 'status':
        item.status = value
    elif key == 'data':
        item.data = value
    item.save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))


@csrf_exempt
def api_api_result_upload(request):
    body = (request.body).decode()
    body_json = eval(urllib.parse.unquote(body))

    if assertAPIARunListObjectIsExist(body_json['data']['Jenkinsid']):
        return HttpResponse(simplejson.dumps({'code': -2, 'msg': '数据库已存在匹配数据'}))
    APIrunlist(Jenkinsid=body_json['data']['Jenkinsid'],
               allNum=body_json['data']['allNum'],
               failNum=body_json['data']['failNum'],
               rt=body_json['data']['rt'],
               ut=body_json['data']['ut'],
               env=body_json['data']['env'],
               type=getValue(body_json['data'], 'type', 0),
               kind=getValue(body_json['data'], 'kind', '全部')
               ).save()
    for item in body_json['data']['result']:
        apiCases(model=getValue(item, 'model'),
                 api=getValue(item, 'api'),
                 case=getValue(item, 'case'),
                 title=getValue(item, 'title'),
                 result=getValue(item, 'res', -1),
                 useTime=getValue(item, 'useTime'),
                 comment=getValue(item, 'comment'),
                 Jenkinsid=body_json['data']['Jenkinsid']).save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))


@csrf_exempt
def api_server_list(request):
    if request.POST:
        type = request.POST['type']
    elif request.GET:
        type = request.GET['type']
    else:
        return simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'})
    objectapi = APIrunlist.objects.filter(type=type).order_by('-id')[0:30]
    Result = {}
    autolist = []

    if objectapi:
        for item in objectapi:
            itemdict = ModelObject.objectAPIList(item)
            autolist.append(itemdict)
    Result['code'] = 0
    Result['msg'] = '成功'
    Result['result'] = autolist
    print(Result)
    return simplejson.dumps(Result)


@csrf_exempt
def api_server_detail(request):
    if request.POST:
        type = request.POST['id']
    elif request.GET:
        type = request.GET['id']
    else:
        return simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'})
    Result = {}
    objectlist = APIrunlist.objects.get(Jenkinsid=type)
    res = ModelObject.objectAPIList(objectlist)
    objectapi = apiCases.objects.filter(Jenkinsid=type)
    caselist = []
    for item in objectapi:
        caselist.append(ModelObject.objectAPICase(item))
    # 排序
    caselist.sort(key=takeRes, reverse=True)
    for i, v in enumerate(caselist):
        if v['result'] != 0:
            pass
        else:
            for j in range(i, len(caselist)):
                for k in range(i, len(caselist)):
                    if takeTime(caselist[j]) > takeTime(caselist[k]):
                        caselist[j], caselist[k] = caselist[k], caselist[j]
            break
    Result['code'] = 0
    Result['msg'] = '成功'
    Result['sum'] = res
    Result['result'] = caselist
    return simplejson.dumps(Result)


def insertReason(request):
    if request.POST:
        type = request.POST['type']
    elif request.GET:
        type = request.GET['type']
    else:
        return HttpResponse(simplejson.dumps({'code': -1, 'msg': '成功'}))
    failReason(reason=type).save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))


def updateReason(request):
    if request.POST:
        type = request.POST['type']
        id = request.POST['id']
    elif request.GET:
        type = request.GET['type']
        id = request.GET['id']
    else:
        return HttpResponse(simplejson.dumps({'code': -1, 'msg': '不支持该类型请求'}))
    item = failReason.objects.get(id=id)
    item.reason = type
    item.save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))


@csrf_exempt
def uploadImg(request):  # 图片上传函数
    if request.method == 'POST':
        imgob = Imgdb(img_url=request.FILES.get('img'))
        imgob.save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))

'''
辅助方法
'''


def assertUiAutoRunListObjectIsExist(id, platform):
    list = uiAutoRunListN.objects.filter(Jenkinsid=id, platform=platform)
    return True if list else False


def assertAPIARunListObjectIsExist(id):
    list = APIrunlist.objects.filter(Jenkinsid=id)
    return True if list else False


def takeRes(el):
    return abs(int(el['result']))


def takeTime(el):
    return abs(int(el['useTime']))


def getValue(item, key, defaultValue=0):
    try:
        return item[key]
    except KeyError as e:
        return defaultValue
