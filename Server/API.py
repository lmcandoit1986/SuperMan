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
from Server.models import resultAll, performanceData, listAPIMointor
from Server.models import CaseDetail, UICaseDetail, uiAutoRunListN
from Server.models import mockData, failReason


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
            reasons.append(case.reason)

    result['detail'].sort(key=takeRes, reverse=True)
    '''
    失败原因
    '''
    result['rD'] = []
    result['rN'] = []
    for line in set(reasons):
        result['rD'].append((failReason.objects.get(id=line).reason))
        result['rN'].append(reasons.count(line))

    result['code'] = 0
    result['msg'] = '成功'

    return simplejson.dumps(result)

@csrf_exempt
def api_auto_list(request):
    objectAndroid = uiAutoRunListN.objects.filter(platform='Android').order_by('-id')[0:7]
    objectiOS = uiAutoRunListN.objects.filter(platform='iOS').order_by('-id')[0:7]

    Result = {
        'Android': {},
        'iOS': {}
    }

    if objectAndroid:
        Result['Android']['rate'] = []
        Result['Android']['list'] = []
        for item in objectAndroid:
            Result['Android']['rate'].append(100 - item.failNum * 100 // item.allNum)
            Result['Android']['list'].append(ModelObject.objectUiAutoRunList(item))
    if objectiOS:
        Result['iOS']['rate'] = []
        Result['iOS']['list'] = []
        for item in objectiOS:
            Result['iOS']['rate'].append(100 - item.failNum * 100 // item.allNum)
            Result['iOS']['list'].append(ModelObject.objectUiAutoRunList(item))

    Result['code'] = 0
    Result['msg'] = '成功'

    return simplejson.dumps(Result)

@csrf_exempt
def api_auto_result_upload(request):
    if request.POST:
        body = (request.body).decode()
        body_json = eval(urllib.parse.unquote(body))
    else:
        return simplejson.dumps({'code': -1, 'msg': '暂不支持该请求方式'})

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
                   appVersion=sum['version'])\
        .save()

    for item in body_json['data']['detail']:
        UICaseDetail(model=item['model'],
                     case=item['case'],
                     caseName=item['caseName'],
                     result=item['result'],
                     useTime=item['useTime'],
                     comment=item['comment'],
                     pic=item['pic'],
                     listid=0,
                     platform=sum['platform'],
                     Jenkinsid=sum['Jenkinsid'],
                     all=item,
                     reason=0)\
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
    print('1')
    if key == 'status':
        item.status = value
    elif key == 'data':
        item.data = value
    item.save()
    return HttpResponse(simplejson.dumps({'code': 0, 'msg': '成功'}))




'''
辅助方法
'''


def assertUiAutoRunListObjectIsExist(id, platform):
    list = uiAutoRunListN.objects.filter(Jenkinsid=id, platform=platform)
    return True if list else False


def takeRes(el):
    return abs(int(el['result']))
