#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
完成 UI 自动化相关的结果上传，下发，修改，更新等操作
'''

import simplejson
from django.views.decorators.csrf import csrf_exempt

from Server import ModelObject
from Server.models import uiAutoRunListN

@csrf_exempt
def api_auto_list(request):
    # 读取
    list_android = uiAutoRunListN.objects.filter(platform='Android').order_by('-id')[0:30]
    list_ios = uiAutoRunListN.objects.filter(platform='iOS').order_by('-id')[0:30]
    # 拼装
    result = {
        'Android': {},
        'iOS': {}
    }

    if list_android:
        result['Android']['rate'] = []
        result['Android']['list'] = []
        for item in list_android:
            if item.allNum == 0:
                result['Android']['rate'].append(0)
            else:
                result['Android']['rate'].append(100 - item.failNum * 100 // item.allNum)
            result['Android']['list'].append(ModelObject.objectUiAutoRunList(item))

    if list_ios:
        result['iOS']['rate'] = []
        result['iOS']['list'] = []
        for item in list_ios:
            if item.allNum != 0:
                result['iOS']['rate'].append(100 - item.failNum * 100 // item.allNum)
            else:
                result['iOS']['rate'].append(0)
            result['iOS']['list'].append(ModelObject.objectUiAutoRunList(item))

    result['code'] = 0
    result['msg'] = '成功'
    return simplejson.dumps(result)