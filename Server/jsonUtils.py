'''
json 相关的处理
'''
import simplejson
from django.http import JsonResponse, HttpResponse

from Server import LogSys


def result(res, isSelf):
    if type(isSelf) == type('str') and (isSelf.lower() == 'true'):
        LogSys.logInfo("独立调用接口:{}".format(res))
        return JsonResponse(res)
    elif type(isSelf) == type('str') and (isSelf.lower() == 'false'):
        LogSys.logInfo("非独立调用接口:{}".format(res))
        return simplejson.dumps(res)
    if isSelf:
        LogSys.logInfo("独立调用接口:{}".format(res))
        return JsonResponse(res)
    LogSys.logInfo("非独立调用接口:{}".format(res))
    return simplejson.dumps(res)
