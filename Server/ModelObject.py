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

from Server.models import resultAll, performanceData, listAPIMointor
from Server.models import CaseDetail, UICaseDetail, uiAutoRunListN
from Server.models import mockData, failReason

'''
object 开头的方法为处理数据表，然后转换为字典输出
'''


def objectUICaseDetail(ob):
    '''
    UICaseDetail 数据表记录转字典
    :param ob:
    :return:
    '''
    result = {}
    result['id'] = ob.id
    result['model'] = ob.model
    result['case'] = ob.case
    result['caseName'] = ob.caseName
    result['result'] = ob.result
    result['useTime'] = ob.useTime
    result['comment'] = ob.comment
    if ob.reason ==0:
        result['reason'] = 1
    '''
    如果使用静态资源，则需要添加图片路径
    '''
    if ob.pic != '':
        if 'png' in ob.pic:
            result['pic'] = 'img/' + ob.pic
        else:
            result['pic'] = 'img/' + ob.pic + '.png'
    else:
        result['pic'] = ob.pic

    return result


def objectUiAutoRunList(object):
    '''
    uiAutoRunListN 数据表记录转字典
    :param ob:
    :return:
    '''
    result = {}
    result['id'] = object.id
    result['allNum'] = object.allNum
    result['failNum'] = object.failNum
    result['device'] = object.device
    result['appVersion'] = object.appVersion
    result['Jenkinsid'] = object.Jenkinsid
    result['appName'] = object.appName
    result['ut'] = object.ut
    result['rt'] = object.rt
    result['platform'] = object.platform
    if object.allNum:
        result['rate'] = 100 - object.failNum * 100 // object.allNum
    else:
        result['rate'] = 0
    result['model'] = object.model
    result['link'] = object.link
    return result

def objectMockDate(item):
    '''
    mockData 数据表记录转字典
    :param item:
    :return:
    '''
    itemdict = {}
    itemdict['id'] = item.id
    itemdict['key'] = item.keyword
    itemdict['api'] = item.api
    itemdict['status'] = item.status
    itemdict['data'] = eval(item.data)
    return itemdict

def objectAPIList(item):
    '''
    APIrunlist 数据表记录转字典
    :param item:
    :return:
    '''
    itemdict = {}
    itemdict['id'] = item.id
    itemdict['Jenkinsid'] = item.Jenkinsid
    itemdict['allNum'] = item.allNum
    itemdict['failNum'] = item.failNum
    itemdict['rt'] = item.rt
    if item.allNum:
        itemdict['rate'] = 100 - item.failNum * 100 // item.allNum
    else:
        itemdict['rate'] = 0
    itemdict['ut'] = item.ut
    return itemdict

def objectAPICase(item):
    '''
    APIrunlist 数据表记录转字典
    :param item:
    :return:
    '''
    itemdict = {}
    itemdict['id'] = item.id
    itemdict['model'] = item.model
    itemdict['api'] = item.api
    itemdict['case'] = item.case
    itemdict['title'] = item.title
    itemdict['result'] = item.result
    itemdict['useTime'] = item.useTime
    itemdict['comment'] = item.comment
    itemdict['Jenkinsid'] = item.Jenkinsid
    return itemdict
