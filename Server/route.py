"""SuperMan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from Server import Server
from SuperMan import settings
from Web import htmlRoute

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'server/result/push',Server.pushResults),
    url(r'server/result/del',Server.delResults),
    url(r'server/result/get',Server.getResults),
    url(r'server/result/list',Server.getResultslist),
    url(r'server/pt/push',Server.pushPerformanceData),
    url(r'server/pt/get',Server.getPtResultsJson),
    url(r'server/result/rate',Server.getRate),
    url(r'server/pt/list',Server.getPTResultslist),

    url(r'web/index',htmlRoute.index),
    url(r'web/list/android',htmlRoute.getAndroidList),
    url(r'web/list/iOS',htmlRoute.getiOSList),
    url(r'web/result/detail',htmlRoute.Deatail),
    url(r'web/result/default',htmlRoute.statistics),
    url(r'web/performance/detail',htmlRoute.performance),
    url(r'web/performance/list/android',htmlRoute.performanceListAndroid),
    url(r'web/performance/list/ios',htmlRoute.performanceListiOS),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)