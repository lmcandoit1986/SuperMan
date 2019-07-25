#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simplejson

from django.http import HttpResponse
from django.shortcuts import render

from Server.models import resultAll, performanceData, listAPIMointor,CaseDetail

def del_listAPIMointor(request):
    id = request.GET.get('id')
    object = listAPIMointor.objects.get(only=id)
    object.delete()
    return HttpResponse(simplejson.dumps(200))
