#!/usr/bin/env python3
# coding=UTF-8
import simplejson

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from Server import Server, API


def result_uiauto_details(request):
    '''
    用于判断编辑条件
    :param request:
    :return:
    '''
    key = 0
    if request.GET['user'] == 'visitor':
        key = 0
    elif request.GET['user'] == 'admin':
        key = 1
    detail = API.api_auto_detail(request)
    detail_dict = simplejson.loads(detail)
    reason = Server.getRealReason(request)
    if detail_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': detail_dict, 'reason': simplejson.loads(reason), 'key': key}

    print(context)

    return render(request, 'uiAutoDetail.html', context)

def result_uiauto_list(request):
    '''
    用于判断编辑条件
    :param request:
    :return:
    '''
    listRun = API.api_auto_list(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}

    print(context)

    return render(request, 'uiAutoList.html', context)