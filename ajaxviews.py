# -*- coding=utf-8 -*-

import json
from django.views import generic
from django.http import HttpResponse  # noqa
from omg_dashboard.api.rest import utils as rest_utils
from horizon.utils.functions import ExceptionCatch
from omg_dashboard.utils import functions as fucApi
from horizon import messages
from django.http import HttpResponseRedirect  
from omg_dashboard.api.sysadmin.workorder import (
                                                    WorkOrderFieldManager,
                                                    WorkOrderEffManager,
                                                    WorkOrderTempManager,
                                                    WorkOrderManager,
                                                    WorkOrderMessageManager
                                                )
from omg_dashboard.api.rest import urls
from django.db.models import Q,Count,Sum
from omg_auth.manager import UserManager
from datetime import datetime,timedelta
from django.conf import settings
from time import strftime
from omg_dashboard.api.dingding import DingApi


def _exception(exc):
    '''
    '''
    LOG.error("{0}: {1}".format(u'请求失败，请重试', exc))
    result = {'result':0, 'error':u'请求失败，请重试'}
    return HttpResponse(json.dumps(result),
                                content_type='application/json')



class CreateFieldView(generic.View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        workorder_field = data.get('workorder_field',None)
        workorder_desc = data.get('workorder_desc',None)
        fieldtype = data.get('fieldtype',None)
        workorder_value = data.get('workorder_value',None)
        reqfield = data.get('reqfield',None)
        data = {}
        objects = WorkOrderFieldManager.add(request,
            reqfield=reqfield,
            workorder_field=workorder_field,
            workorder_desc=workorder_desc,
            fieldtype=fieldtype,
            workorder_value=workorder_value)
        if objects:
            data = {'result':1,'msg':u'添加字段成功'}
        else:
            data = {'result':2,'msg':u'添加字段失败'}
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


class GetOrderView(generic.View):

    def get(self, request, *args, **kwargs):
        orderId = request.GET.get('id')
        # objects = WorkOrderManager.get(request,
        #     id=orderId
        #     )
        # if objects:
        #     data={'status':objects.status}
        # else:
        data={}
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


class UpdateFieldView(generic.View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        workorder_field = data.get('workorder_field',None)
        workorder_desc = data.get('workorder_desc',None)
        fieldtype = data.get('fieldtype',None)
        workorder_value = data.get('workorder_value',None)
        fieldid = data.get('field',None)
        reqfield = data.get('reqfield',None)
        data = {}
        objects = WorkOrderFieldManager.update(request,
            reqfield=reqfield,fieldid=fieldid,
            workorder_field=workorder_field,
            workorder_desc=workorder_desc,
            fieldtype=fieldtype,
            workorder_value=workorder_value)
        if objects:
            data = {'result':1,'msg':u'编辑字段成功'}
        else:
            data = {'result':2,'msg':u'编辑字段失败'}
        return HttpResponse(json.dumps(data),
                            content_type='application/json')

class CreateOrderView(generic.View):

    def post(self, request, *args, **kwargs):
        data = request.POST

        order_name = data.get('order_name',None)
        order_desc = data.get('order_desc',None)
        field_obj = json.loads(data.get('field_obj',None))
        temp_id = data.get('temp_id',None)
        send_cc = json.loads(data.get('order_cc',None))
        userid = data.get('userid',None)
        files = request.FILES.getlist('files')
        tempobj = WorkOrderTempManager.get('',id=temp_id)
        time_now = strftime("%Y-%m-%d %H:%M")
        attachment = []
        send_user_id = []
        data = {}
        try:
            groups = UserManager.get(id=int(userid))
        except Exception:
            pass
        order_group = [int(o.id) for o in tempobj.auditgroup.all()]
        user_group = [int(o.id) for o in groups.groupname.all()]
        result = list(set(user_group).intersection(set(order_group)))
        user_obj = UserManager.filter(groupname__in=result,is_headman=True)
        if len(user_obj) == 0:
            data = {'result':False,'msg':u'请联系管理员把你加入某个组里面'}
        if files:
            UPLOAD_PATH = getattr(settings, 'UPLOAD_PATH')
            key_path = fucApi.joinpath(UPLOAD_PATH,str('workorder'),str(userid))
            key_path = fucApi.mkdir(key_path)
            for file in files:
                attachment.append({'name':file.name,'path':key_path})
                destfile = open(key_path + '/' + file.name,'w')
                for chunk in file.chunks():
                    destfile.write(chunk)

        kwargs = {
            'userid':userid,
            'hidestatus':1,
            'name':order_name,
            'description':order_desc,
            'ordertemp':tempobj,
            'orderfield':json.dumps(field_obj),
            'attachment':json.dumps(attachment),
        }
        try:
            objects = WorkOrderManager.add(request,**kwargs)
            data = {'result':True,'msg':u'创建工单成功','id':objects.id}
            if tempobj and tempobj.is_audit:
                message = '待审核工单：[ {0} ]'.format(tempobj.name)
            else:
                message = '待处理工单 [ {0} ]　'.format(tempobj.name)
            obj_msg = WorkOrderMessageManager.insert(orderid=objects,message=message,userid=userid)
            obj_msg.save()
            for user in send_cc:
                try:
                    userobj = UserManager.get(id=user)
                    send_user_id.append(userobj.userId)
                    objects.ccusers.add(userobj)
                except Exception:
                    pass
            for user in tempobj.ccusers.all():
                try:
                    send_user_id.append(user.userId)
                except Exception:
                    pass
            for user in user_obj:
                try:
                    send_user_id.append(user.userId)
                    objects.auditusers.add(user)
                except Exception:
                    pass
            if send_user_id:
                body = {}
                body['user'] = set(send_user_id)
                request_url = "http://{0}/sysadmin/workorder/{1}/list".format(request.get_host(),objects.id)
                body['msg'] = '工单编号:{0}\n主题:{1}\n描述:{2}\n来自:{3}\n时间:{4}\n访问地址:{5}\n'.format(
                    objects.id,tempobj.name,tempobj.description,
                    UserManager.get(id=userid).username,
                    time_now,request_url)
                api = DingApi()
                try:
                    api.senddingText(body['user'],body['msg'])
                except Exception:
                    pass
        except Exception:
            pass
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


class OrderMessageView(generic.View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        orderId = data.get('orderId',None)
        message = data.get('message',None)
        status = data.get('status',None)
        user = data.get('user',None)
        hidestatus = data.get('hidestatus',None)
        data = {}
        user_obj = self.request.user.id
        objects = WorkOrderMessageManager.add(request,\
            orderId=orderId,message=message,userid=user_obj,\
            status=status,user=user,hidestatus=hidestatus)
        if objects:
            data = {'result':1,'msg':u'信息发送成功','id':objects.id}
        else:
            data = {'result':2,'msg':u'信息发送失败'}
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


class OrderDeleteView(generic.View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        orderId = data.get('orderId',None)
        data = {}
        objects = WorkOrderManager.delete(orderId)
        if objects:
            data = {'result':1,'msg':u'工单删除成功'}
        else:
            data = {'result':2,'msg':u'工单删除失败'}
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


class ListTempView(generic.View):

    @ExceptionCatch(_exception)
    @rest_utils.ajax()
    def get(self,request,*arg,**kwargs):
        data = json.loads(request.body)
        tempTypeId = data.get('id',None)
        objects = WorkOrderManager.list(ordertemp=tempTypeId)
        return HttpResponse(json.dumps(objects),
                content_type='application/json')            


class EfficiencyView(generic.View):

    @ExceptionCatch(_exception)
    @rest_utils.ajax()
    def get(self,request,*arg,**kwargs):
        begintime = request.GET.get('begintime', None)
        endtime = request.GET.get('endtime', None)
        if begintime is None:
            begintime = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d %H:%M:%S')
        if endtime is None:
            endtime = (datetime.now() + timedelta(days=0)).strftime('%Y-%m-%d %H:%M:%S')
        users = []
        weekUsers = []
        orderDealTime = []
        effObject = []
        weekDealTime = []
        orders = WorkOrderManager.count(delete=False)
        openOrders = WorkOrderManager.count(status=0) 
        ordObjects = WorkOrderManager.list(request).exclude(status=0)\
            .filter(addedtime__gte=begintime,addedtime__lte=endtime)
        effObjects = WorkOrderEffManager.list()

        weekOrderObjects = WorkOrderManager.list('',addedtime__gte=begintime,addedtime__lte=endtime)\
            .exclude(status=0).exclude(status=3).values('confirmuser').annotate(count=Count('confirmuser'))
        for obj in weekOrderObjects:
            if obj['confirmuser']:
                try:
                    weekUsers.append({
                            'username':UserManager.get(id=obj['confirmuser']).username,
                            'count':obj['count'],
                            }
                        )
                except Exception:
                    pass
        weekOrderObjects = WorkOrderManager.list('',addedtime__gte=begintime,addedtime__lte=endtime)\
            .exclude(status=0).exclude(status=3).values('confirmuser').annotate(sum=Sum('dealtime'))
        for obj in weekOrderObjects:
            if obj['confirmuser']:
                try:
                    weekDealTime.append({
                            'username':UserManager.get(id=obj['confirmuser']).username,
                            'sum':obj['sum'],
                        })
                except Exception:
                    pass
        if effObjects:
            for obj in effObjects:
                effObject.append({'time':obj.addedtime.strftime('%Y-%m-%d %H:%M:%S'),'value':obj.value})
        if ordObjects:
            for obj in ordObjects:
                orderDealTime.append({'time':obj.dealtime,'id':obj.id})
        userObj = WorkOrderManager.group('confirmuser')
        for obj in userObj:
            if obj['confirmuser']:
                try:
                    users.append({
                            'username':UserManager.get(id=obj['confirmuser']).username,
                            'count':obj['count'],
                            })
                except Exception:
                    pass
        objects = {
            'effObject':effObject,
            'users':users,
            'weekUsers':weekUsers,
            'orders':orders,
            'openorders':openOrders,
            'orderDealTime':orderDealTime,
            'weekDealTime':weekDealTime,
            }
        return HttpResponse(json.dumps(objects),
                content_type='application/json') 