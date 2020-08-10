#!/usr/bin/env python3
# coding=UTF-8
import simplejson

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from Server import Server, API, LogSys


def result_uiauto_details(request):
    '''
    用于判断编辑条件
    :param request:
    :return:
    '''
    LogSys.logInfo('Request:{0}'.format(request))
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
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'uiAutoDetail.html', context)

def result_uiauto_list(request):
    '''
    用于判断编辑条件
    :param request:
    :return:
    '''
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_auto_list(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'uiAutoList.html', context)

def result_apicheck_list(request):
    '''
    :param request:
    :return:
    '''
    LogSys.logInfo('API:web/result/api/monitor')
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_server_list(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'apiMonitor.html', context)

def result_api_detail(request):
    '''
    :param request:
    :return:
    '''
    LogSys.logInfo('API:web/result/api/detail')
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_server_detail(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'APIDetail.html', context)

def v2_ui_list(request):
    '''
    :param request:
    :return:
    '''
    '''
        用于判断编辑条件
        :param request:
        :return:
        '''
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_auto_list(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_uiauto_list.html', context)

def v2_api_auto_list(request):
    '''
    :param request:
    :return:
    '''
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_server_list(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_api_auto_list.html', context)

def v2_mock_insert(request):
    LogSys.logInfo('Request:{0}'.format(request))
    t = get_template('basis_mock_insert.html')
    html = t.render()
    return HttpResponse(html)

def v2_mock_manager(request):
    LogSys.logInfo('Request:{0}'.format(request))
    res = Server.mock_data_list(request)
    res_dict = eval(res)
    context = {'person': res_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_mock_manager.html', context)

def v2_ui_detail(request):
    '''
    用于判断编辑条件
    :param request:
    :return:
    '''
    LogSys.logInfo('Request:{0}'.format(request))
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
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_uiauto_detail.html', context)

def v2_api_auto_detail(request):
    '''
    :param request:
    :return:
    '''
    LogSys.logInfo('API:web/result/api/detail')
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = API.api_server_detail(request)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_api_detail.html', context)