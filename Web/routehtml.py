#!/usr/bin/env python3
# coding=UTF-8
import re

import simplejson

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from Server import Server, API, LogSys, ServerUI


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
    LogSys.logInfo('Request:{0}'.format(request))
    listRun = ServerUI.api_auto_list(request)
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
    user_agent = request.META['HTTP_USER_AGENT']
    detail = API.api_auto_detail(request)
    detail_dict = simplejson.loads(detail)
    reason = Server.getRealReason(request)
    if detail_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': detail_dict, 'reason': simplejson.loads(reason), 'key': key}
    LogSys.logInfo('Result:{0}'.format(context))
    if re.search('iPhone|iPod|Android|ios|iOS|iPad|Backerry|WebOS|Symbian|Windows Phone|Phone',user_agent):
        return render(request, 'basis_uiauto_detail_h5.html', context)
    else:
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

def v2_api_ci_control_list(request):
    '''
    :param request:
    :return:
    '''
    LogSys.logInfo('API:web/result/api/detail')
    listRun = Server.CIControlList(request)
    print(listRun)
    listRun_dict = simplejson.loads(listRun)
    if listRun_dict['code'] != 0:
        context = {'person': None}
    else:
        context = {'person': listRun_dict}
    LogSys.logInfo('Result:{0}'.format(context))
    return render(request, 'basis_ci_control.html', context)

def case_android_list(request):
    res_class = Server.search_db_class(request)
    res_case = Server.search_db_case(request)
    data ={'class':eval(res_class), 'case':eval(res_case)}
    return render(request, 'basis_cases_android.html', data)


def job_list(request):
    jobs = Server.search_db_job(request)
    return render(request, 'basis_job.html', eval(jobs))