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

from Server import Server, views, API
from SuperMan import settings
from Web import htmlRoute, routehtml

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'server/result/push$',Server.pushResults),
    url(r'server/result/v2/push$',Server.pushResultsV2),
    url(r'server/result/v3/push$',Server.pushResultsV3),
    url(r'server/result/del$',Server.delResults),
    url(r'^mock/data/insert$',Server.mock_data_insert),
    url(r'^mock/data/del$',Server.mock_data_del),
    url(r'^mock/data/status/change$', Server.mock_data_status_change),
    url(r'^mock/data/edit$', Server.mock_data_edit),
    url(r'^mock/data/by/api$', Server.mock_data_get_by_api),
    url(r'^mock/data/by/api/key', Server.mock_data_get_by_api_key),  # 获取mock 匹配数据,通过api 和key 筛选,过滤失效的数据
    url(r'^mock/data/by/id$',Server.mock_data_get_by_id), # 获取mock 匹配数据，通过 id 筛选,不过滤
    url(r'^server/bank/ms/invest$',Server.investMSBank),
    url(r'server/result/get$',Server.getResults),
    url(r'server/reason/get$',Server.getRealReason),
    url(r'server/reason/set$',Server.setRealReason),
    url(r'server/result/list$',Server.getResultslist),
    url(r'server/result/v3/list$', Server.getListResultNew),
    url(r'server/result/listJson$',Server.getResultslistJson),
    url(r'server/pt/push$',Server.pushPerformanceData),
    url(r'server/pt/get$',Server.getPtResultsJson),
    url(r'server/result/rate$',Server.getRate),
    url(r'server/pt/list$',Server.getPTResultslist),
    url(r'server/monitor/push$',Server.pushMonitorResults),
    url(r'server/monitor/get$',Server.getAPIMonitorDataJson),
    url(r'server/monitor/list$',Server.getAPIMonitorRateJson),
    url(r'server/monitor/del$',views.del_listAPIMointor),

    url(r'^api/uiauto/result/upload$', API.api_auto_result_upload),  # 测试结果上传
    url(r'^api/insert/fail/reason$', API.insertReason),  # 测试结果上传
    url(r'^api/mock/data/edit$', API.api_mock_data_edit),  # 测试结果上传
    url(r'^api/uiauto/result/del$', API.api_auto_detail_del),  # 测试结果上传
    url(r'^api/server/result/upload$', API.api_api_result_upload),  # 测试结果上传
    url(r'^api/fail/reason/get$', Server.getRealReasonHttp),  # 测试结果上传
    url(r'^api/fail/reason/update$', API.updateReason),
    url(r'^api/img/upload$', API.uploadImg),  # 测试结果上传

    url(r'web/watcher$',htmlRoute.APIWatcher),
    url(r'web/uiAuto$',htmlRoute.uiauto),
    url(r'web/mock$',htmlRoute.new),
    url(r'web/list/mock$',htmlRoute.mocklist),
    url(r'web/uiAutoDetail$',htmlRoute.Deatailv3),
    url(r'web/index$',htmlRoute.index),
    url(r'web/sms$',htmlRoute.sms),
    url(r'web/error$',htmlRoute.error),
    url(r'web/list/android$',htmlRoute.getAndroidList),
    url(r'web/list/iOS$',htmlRoute.getiOSList),
    url(r'web/result/detail$',htmlRoute.Deatail),
    url(r'web/result/v2/detail$',htmlRoute.Deatailv2),
    url(r'web/result/v3/detail$',htmlRoute.Deatailv3),
    url(r'web/result/default$',htmlRoute.statistics),
    url(r'web/performance/detail$',htmlRoute.performance),
    url(r'web/performance/v2/detail$',htmlRoute.performanceList),
    url(r'web/performance/list/android$',htmlRoute.performanceListAndroid),
    url(r'web/performance/list/ios$',htmlRoute.performanceListiOS),
    url(r'web/api/monitor/list$',htmlRoute.getAPIMonitorList),

    url(r'^web/result/uiauto/detail$', routehtml.result_uiauto_details),
    url(r'^web/result/uiauto/list$', routehtml.result_uiauto_list),
    url(r'^web/result/api/monitor$', routehtml.result_apicheck_list),
    url(r'^web/result/api/detail$', routehtml.result_api_detail),

    url(r'^api/web/ui/list$', routehtml.v2_ui_list),  # ui自动化结果列表
    url(r'^api/web/api/list$', routehtml.v2_api_auto_list),  # api 自动化结果列表
    url(r'^api/web/mock/insert$', routehtml.v2_mock_insert),
    url(r'^api/web/mock/manager$', routehtml.v2_mock_manager),
    url(r'^api/web/ui/detail$', routehtml.v2_ui_detail),
    url(r'^api/web/api/detail$', routehtml.v2_api_auto_detail),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)