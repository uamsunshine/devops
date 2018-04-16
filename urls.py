# -*- coding=utf-8 -*-
from django.conf.urls import patterns
from django.conf.urls import url
from omg_dashboard.dashboards.sysadmin.workorder import views
from omg_dashboard.dashboards.sysadmin.workorder import ajaxviews


urlpatterns = patterns(
    'omg_dashboard.dashboards.sysadmin.workorder.views',
    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'^(?P<id>[^/]+)/createfieldtype/$',views.CreateFieldTypeView.as_view(),name='createfieldtype'),
    url(r'fieldtype/$',views.FieldTypeView.as_view(),name='fieldtype'),
    url(r'field/$',views.FieldView.as_view(),name='field'),
    url(r'field/create',ajaxviews.CreateFieldView.as_view(),name='json_field_create'),
    url(r'^(?P<id>[^/]+)/field/update/$',views.UpdateFieldView.as_view(),name='updatefield'),
    url(r'field/update',ajaxviews.UpdateFieldView.as_view(),name='json_field_update'),
    url(r'temp/$',views.WorkOrderTempView.as_view(),name='workordertemp'),
    url(r'temp/list/$',views.ListTempView.as_view(),name='listtemp'),
    url(r'(?P<id>[^/]+)/type/list/$',views.ListTypeTempView.as_view(),name='listtypetemp'),
    url(r'temp/create/$',views.CreateTempView.as_view(),name='createtemp'),
    url(r'(?P<id>[^/]+)/temp/update/$',views.UpdateTempView.as_view(),name='updatetemp'),
    url(r'temp/type/$',views.WorkOrderTempTypeView.as_view(),name='temptype'),
    url(r'temp/type/create/$',views.CreateTempTypeView.as_view(),name='createtemptype'),
    url(r'^(?P<id>[^/]+)/temp/type/update/$',views.UpdateTempTypeView.as_view(),name='updatetemptype'),
    url(r'(?P<id>[^/]+)/order/$',views.CreateOrderView.as_view(),name='createorder'),
    # url(r'(?P<id>[^/]+)/order/$',views.CreateOrderView.as_view(),name='createorder'),
    # url(r'order/get',ajaxviews.GetOrderView.as_view(),name='json_get_order'),
    url(r'order/create',ajaxviews.CreateOrderView.as_view(),name='json_create_order'),
    url(r'(?P<id>[^/]+)/list/$',views.ListOrderView.as_view(),name='listorder'),
    url(r'(?P<id>[^/]+)/edit/$',views.EditOrderView.as_view(),name='editorder'),
    url(r'order/message',ajaxviews.OrderMessageView.as_view(),name='json_order_message'),
    url(r'order/delete',ajaxviews.OrderDeleteView.as_view(),name='json_order_delete'),
    url(r'efficiency/$',views.EfficiencyView.as_view(),name='efficiency'),
    url(r'efficiency/list',ajaxviews.EfficiencyView.as_view(),name='efflist'),

)
