# -*- coding=utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render_to_response
from django.views import generic
from horizon import exceptions, tables, forms, tabs
from horizon.utils import memoized
from horizon.utils import functions as utils
from horizon import workflows
from django.views import generic
import json,urllib2

from django.views.generic.base import TemplateView
from omg_dashboard.dashboards.sysadmin.workorder.tables import ListTempTable,WorkOrderTable,WorkOrderFieldTable,WorkOrderFieldTypeTable,WorkOrderTempTable,WorkOrderTempTypeTable
from omg_dashboard.api.sysadmin.workorder import WorkOrderMessageManager,WorkOrderManager,WorkOrderFieldManager,WorkOrderFieldTypeManager,WorkOrderTypeManager,WorkOrderTempManager
from omg_dashboard.dashboards.sysadmin.workorder.forms import CreateTempTypeForm,CreateTempForm,UpdateTempTypeForm,UpdateTempForm,OrderUpdateForm
from omg_dashboard.dashboards.sysadmin.models import WORK_ORDER_TEMP_PRIORITY,ICON,WORK_ORDER_STATUS
from omg_auth.manager import UserManager,UserGroupManager



class IndexView(tables.DataTableView):
    table_class = WorkOrderTable
    template_name = 'sysadmin/workorder/index_workorder.html'
    page_title = u"我的工单"

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def totalcount(self, table):
        return self._totalcount

    def get_data(self):
        search_opts = {}
        filter = self.get_server_filter_info(self.request)
        if filter['value'] and filter['field']:
                search_opts = {filter['field']: filter['value']}
        marker = self.request.GET.get(WorkOrderTable._meta.pagination_param, None)
        args = {'marker': marker, 'paginate': True,'filters':'','sort_dir':'desc'}
        objs = WorkOrderManager.filter(self.request,search_opts=search_opts)
        objects, self._prev, self._more = utils.paginate(
            self.request,
            objs,
            **args
        )
        self._totalcount = len(objs)
        return objects


class FieldView(tables.DataTableView):
    table_class = WorkOrderFieldTable
    template_name = 'sysadmin/workorder/index_workorder_field.html'
    page_title = u"工单字段"

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        search_opts = {}
        filter = self.get_server_filter_info(self.request)
        if filter['value'] and filter['field']:
                search_opts = {filter['field']: filter['value']}
        marker = self.request.GET.get(WorkOrderFieldTable._meta.pagination_param, None)
        args = {'marker': marker, 'paginate': True,'filters':'','sort_dir':'desc'}
        objects, self._prev, self._more = utils.paginate(
            self.request,
            WorkOrderFieldManager.list(self.request,search_opts=search_opts),
            **args
        )
        return objects

class UpdateFieldView(TemplateView):
    template_name = "sysadmin/workorder/update_field.html"
    page_title = u"修改工单字段"

    def get_context_data(self,**kwargs):
        fieldid = kwargs['id']
        context = super(UpdateFieldView, self).get_context_data(**kwargs)
        field_obj = WorkOrderFieldManager.get(self.request,fieldid=fieldid)
        context['field'] = {'id':field_obj.id,'name':field_obj.name,
            'value':json.loads(field_obj.value),'description':field_obj.description,
            'fieldid':field_obj.fieldtype.id}        
        if field_obj.fieldtype.temp == 1:
            context['value'] = [{'id':v['id'],'name':v['name']} for v in json.loads(field_obj.value)]
            self.template_name ="sysadmin/workorder/update_choice_field.html"
        return context


class FieldTypeView(tables.DataTableView):
    table_class = WorkOrderFieldTypeTable
    template_name = 'sysadmin/workorder/index_workorder_field_type.html'
    page_title = u"工单字段类型"

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        marker = self.request.GET.get(WorkOrderFieldTypeTable._meta.pagination_param, None)
        args = {'marker': marker, 'paginate': True,'filters':'','sort_dir':'desc'}
        objects, self._prev, self._more = utils.paginate(
            self.request,
            WorkOrderFieldTypeManager.list(self.request),
            **args
        )
        return objects    


class CreateFieldTypeView(TemplateView):
    template_name = "sysadmin/workorder/create_field.html"
    page_title = u"添加工单字段"

    def get_context_data(self,**kwargs):
        fieldtypeid = kwargs['id']
        context = super(CreateFieldTypeView, self).get_context_data(**kwargs)
        context['field_type'] = WorkOrderFieldTypeManager.get(self.request,id=fieldtypeid)
        if context['field_type'].temp == 1:
            self.template_name ="sysadmin/workorder/create_choice_field.html"
        return context


class WorkOrderTempView(tables.DataTableView):
    table_class = WorkOrderTempTable
    template_name = 'sysadmin/workorder/index_workorder_temp.html'
    page_title = u"工单模板"

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        search_opts = {}
        filter = self.get_server_filter_info(self.request)
        if filter['value'] and filter['field']:
                search_opts = {filter['field']: filter['value']}
        marker = self.request.GET.get(WorkOrderTempTable._meta.pagination_param, None)
        args = {'marker': marker, 'paginate': True,'filters':'','sort_dir':'desc'}
        objects, self._prev, self._more = utils.paginate(
            self.request,
            WorkOrderTempManager.list(self.request,search_opts=search_opts),
            **args
        )
        return objects


class WorkOrderTempTypeView(tables.DataTableView):
    table_class = WorkOrderTempTypeTable
    template_name = 'sysadmin/workorder/temp_type.html'
    page_title = u"工单模板类型"

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        marker = self.request.GET.get(WorkOrderTempTypeTable._meta.pagination_param, None)
        args = {'marker': marker, 'paginate': True,'filters':'','sort_dir':'desc'}
        objects, self._prev, self._more = utils.paginate(
            self.request,
            WorkOrderTypeManager.list(self.request),
            **args
        )
        return objects

class CreateTempTypeView(forms.ModalFormView):
    form_class = CreateTempTypeForm
    form_id = "create_temp_form"
    template_name = 'sysadmin/workorder/create_temp_type.html'
    page_title = u'新建模板类型'
    cancel_label = u'取消'
    submit_label = u'新建'
    submit_url = 'horizon:sysadmin:workorder:createtemptype'
    success_url = reverse_lazy("horizon:sysadmin:workorder:temptype")

    def get_context_data(self, **kwargs):
        context = super(CreateTempTypeView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class CreateTempView(forms.ModalFormView):
    form_class = CreateTempForm
    form_id = "create_temp_form"
    template_name = 'sysadmin/workorder/create_temp.html'
    page_title = u'新建模板'
    cancel_label = u'取消'
    submit_label = u'新建'
    submit_url = 'horizon:sysadmin:workorder:createtemp'
    success_url = reverse_lazy("horizon:sysadmin:workorder:workordertemp")

    def get_context_data(self, **kwargs):
        context = super(CreateTempView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context

    def get_initial(self):
        data = {
            'is_audit':(0),
            'is_cc':(0),
            'is_attachment':(0),
            'is_confirm':(0),
        }
        return data

class UpdateTempView(forms.ModalFormView):
    form_class = UpdateTempForm
    form_id = "update_temp_form"
    template_name = 'sysadmin/workorder/update_temp.html'
    page_title = u'修改模板'
    cancel_label = u'取消'
    submit_label = u'更新'
    submit_url = 'horizon:sysadmin:workorder:updatetemp'
    success_url = reverse_lazy("horizon:sysadmin:workorder:workordertemp")

    def get_object(self):
        id = self.kwargs.get('id', None)
        return WorkOrderTempManager.get(self.request,id=id)

    def get_context_data(self, **kwargs):
        context = super(UpdateTempView, self).get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        temp = self.get_object()
        if temp.is_audit:
            is_audit = (1)
        else:
            is_audit = (0)
        if temp.is_cc:
            is_cc = (1)
        else:
            is_cc = (0)
        if temp.is_attachment:
            is_attachment = (1)
        else:
            is_attachment = (0)
        if temp.is_confirm:
            is_confirm = (1)
        else:
            is_confirm = (0)
        data = {
            'tempobj':temp,
            'name': unicode(temp.name),
            'description':unicode(temp.description),
            'temptype':temp.typeid.id,
            'field':[item.id for item in temp.fieldid.all()],
            'cc':[ item.id for item in temp.ccusers.all()],
            'auditgroup':[item.id for item in temp.auditgroup.all()],
            'tousers':[item.id for item in temp.tousers.all()],
            'is_audit':is_audit,
            'is_cc':is_cc,
            'is_attachment':is_attachment,
            'is_confirm':is_confirm,
        }
        return data


class UpdateTempTypeView(forms.ModalFormView):
    form_class = UpdateTempTypeForm
    form_id = "update_temp_type_form"
    template_name = 'sysadmin/workorder/update_temp_type.html'
    page_title = u'修改模板类型'
    cancel_label = u'取消'
    submit_label = u'修改'
    submit_url = 'horizon:sysadmin:workorder:updatetemptype'
    success_url = reverse_lazy("horizon:sysadmin:workorder:temptype")

    def get_object(self):
        id = self.kwargs.get('id', None)
        return WorkOrderTypeManager.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(UpdateTempTypeView, self).get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        temptype = self.get_object()
        data = {
            'name': unicode(temptype.name),
            'icon': temptype.icon,
            'description': temptype.description,
        }
        return data

class EditOrderView(forms.ModalFormView):
    form_class = OrderUpdateForm
    form_id = "order_update_form"
    template_name = 'sysadmin/workorder/update_temp.html'
    page_title = u'更新审核人'
    cancel_label = u'取消'
    submit_label = u'更新'
    submit_url = 'horizon:sysadmin:workorder:editorder'
    success_url = reverse_lazy("horizon:sysadmin:workorder:index")

    def get_context_data(self, **kwargs):
        context = super(EditOrderView, self).get_context_data(**kwargs)
        args = (self.kwargs['id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_object(self):
        id = self.kwargs.get('id', None)
        return WorkOrderManager.get('',id=id)

    def get_initial(self):
        orderobj = self.get_object()
        data = {
            'cc':[ item.id for item in orderobj.ccusers.all()],
            'audituser':[ item.id for item in orderobj.auditusers.all()],
        }
        return data


class CreateOrderView(TemplateView):
    template_name = "sysadmin/workorder/create_order.html"
    page_title = u"提交工单"

    def get_context_data(self,**kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        tempid = kwargs['id']
        userid = self.request.user.id
        temp_obj = WorkOrderTempManager.get(self.request,id=tempid)
        fields = []
        field_num = []
        priority = []
        for item in temp_obj.fieldid.all():
            fields.append({'id':item.id,'value':json.loads(item.value),
                'name':item.name,'description':item.description,
                'fieldtype':item.fieldtype})
            field_num.append({'id':int(item.id)})
        context['fields'] = fields
        context['field_num'] = field_num
        context['temp_obj'] = temp_obj
        context['userid'] = userid
        cc = []

        for user in UserManager.list():
            cc.append({'id':str(user['id']),
                    'username':str(user['username'])})
        context['cc'] = cc

        for p in WORK_ORDER_TEMP_PRIORITY:
            if p[0] == 0:
                priority.append({'name':p[1],'value':p[0],'checked':'checked'})
            else:
                priority.append({'name':p[1],'value':p[0],'checked':''})
        context['priority'] = priority
        return context


class ListTempView(TemplateView):
    template_name = 'sysadmin/workorder/list_temp.html'
    page_title = u"提交工单"

    def get_context_data(self,**kwargs):
        context = super(ListTempView,self).get_context_data(**kwargs)
        temp_type_obj = []
        for i in WorkOrderTypeManager.list(self.request):
            temp_obj = []
            temp = WorkOrderTempManager.filter(self.request,typeid=i.id)
            if temp:
                for s in temp:
                    temp_obj.append({'name':s.name,'id':s.id})
                temp_type_obj.append({
                        'isExist':True,
                        'name':i.name,
                        'id':i.id,
                        'temp_obj':temp_obj,
                        'icon':WorkOrderTypeManager.getIcon(id=i.icon)
                        })
            else:
                temp_type_obj.append({'name':i.name,'id':i.id,'isExist':False})
        context['temp_type_obj'] = temp_type_obj
        return context


class ListTypeTempView(TemplateView):
    template_name = "sysadmin/workorder/list_type_temp.html"
    page_title = u"显示工单模板"

    def get_context_data(self,**kwargs):
        typeid = kwargs['id']
        context = super(ListTypeTempView, self).get_context_data(**kwargs)
        context['temp_obj'] = WorkOrderTempManager.filter(self.request,typeid=typeid)
        return context


class EfficiencyView(TemplateView):
    template_name = "sysadmin/workorder/eff.html"
    page_title = u"显示工单模板"

    def get_context_data(self,**kwargs):
        context = super(EfficiencyView, self).get_context_data(**kwargs)
        # context['temp_obj'] = WorkOrderTempManager.filter(self.request,typeid=typeid)
        return context


class ListOrderView(TemplateView):
    template_name = "sysadmin/workorder/list_order.html"
    page_title = u"工单详情"

    def get_context_data(self,**kwargs):
        orderid = kwargs['id']
        context = super(ListOrderView, self).get_context_data(**kwargs)
        order_obj = WorkOrderManager.get(self.request,id=orderid)
        userid = self.request.user.id
        user_obj = UserManager.get(id=self.request.user.id)
        if order_obj and user_obj:
            message_obj = WorkOrderMessageManager.get(self.request,
                orderid=WorkOrderManager.get(self.request,id=orderid))
            mesg_obj = []
            if message_obj:
                for item in message_obj:
                    if item.attachment:
                        mesg_obj.append({'avatar':UserManager.get(id=item.userid).avatar,
                            'username':UserManager.get(id=item.userid).username,
                            'message':item.message,'attachment':json.loads(item.attachment),
                            'addedtime':item.addedtime})
                    else:
                        mesg_obj.append({'avatar':UserManager.get(id=item.userid).avatar,
                            'username':UserManager.get(id=item.userid).username,
                            'message':item.message,'addedtime':item.addedtime})
            context['mesg_obj'] = mesg_obj

            self.page_title = u"工单详情"
            context['field_obj'] = json.loads(order_obj.orderfield)
            if order_obj.attachment:
                context['order_attachment'] = json.loads(order_obj.attachment)
            context['order_obj'] = order_obj
            context['status'] = WorkOrderManager.get_status(order_obj.status)
            
            send_cc = []
            send_user = []
            if order_obj.ordertemp.ccusers:
                for user in order_obj.ordertemp.ccusers.all():
                    send_cc.append(int(user.id))
                    send_user.append(user.userId)
            if order_obj.ccusers:
                for user in order_obj.ccusers.all():
                    send_cc.append(int(user.id))
                    send_user.append(user.userId)

            if order_obj.auditusers:
                for user in order_obj.auditusers.all():
                    send_cc.append(int(user.id))
                    send_user.append(user.userId)

            context['send_handle_user'] = json.dumps(send_user)
            if UserManager.get(id=order_obj.userid).userId:
                context['send_order_user'] = json.dumps(
                    [str(UserManager.get(id=order_obj.userid).userId)])
            else:
                context['send_order_user'] = json.dumps([])
            context['userid'] = user_obj.id
            context['username'] = UserManager.get(id=int(order_obj.userid)).username
            context['orderUserId'] = order_obj.userid

            if order_obj.ordertemp.is_audit is True:
                self.template_name = "sysadmin/workorder/list_audit_order.html"

                if int(order_obj.status) == 0:
                    context['openstatus'] = 'active'
                if int(order_obj.status) == 1:
                    context['confirmstatus'] = 'active'
                if int(order_obj.status) == 2:
                    context['closestatus'] = 'active'
                if int(order_obj.status) == 4:
                    context['auditstatus'] = 'active'
                if int(order_obj.status) == 5:
                    context['repulsestatus'] = 'active'
                if int(order_obj.status) == 0  and user_obj.id in [int(user.id) for user in order_obj.auditusers.all()]:
                    context['auditpassed'] = True
                    context['repulse'] = True
                if user_obj.id in [int(user.id) for user in order_obj.ordertemp.ccusers.all()] and int(order_obj.status) == 4:
                    context['confirm'] = True
                    context['repulse'] = True
                if user_obj.id == order_obj.userid and int(order_obj.status) == 1:
                    context['close'] = True


                if int(order_obj.status) == 2 or int(order_obj.status) == 0:
                    context['disabled'] = 'none'
                elif user_obj.id == order_obj.userid:
                    context['disabled'] = ''
                if int(order_obj.status) == 0 and order_obj.userid == user_obj.id:
                    context['disabled'] = ''
                if int(order_obj.status) == 5 and order_obj.userid == user_obj.id:
                    context['disabled'] = 'none'
            elif order_obj.ordertemp.is_confirm is True:
                self.template_name = "sysadmin/workorder/list_audit_order.html"
                if int(order_obj.status) == 0:
                    context['openstatus'] = 'active'
                if int(order_obj.status) == 1:
                    context['confirmstatus'] = 'active'
                if int(order_obj.status) == 2:
                    context['closestatus'] = 'active'
                if int(order_obj.status) == 4:
                    context['auditstatus'] = 'active'
                if int(order_obj.status) == 5:
                    context['repulsestatus'] = 'active'

                if  int(order_obj.status) == 0  and user_obj.id in [int(user.id) for user in order_obj.ordertemp.tousers.all()]:
                    context['auditpassed'] = True
                    context['repulse'] = True
                if user_obj.id in [int(user.id) for user in order_obj.ordertemp.ccusers.all()] and int(order_obj.status) == 4:
                    context['confirm'] = True
                    context['repulse'] = True
                if user_obj.id == order_obj.userid and int(order_obj.status) == 1:
                    context['close'] = True


                if int(order_obj.status) == 2 or int(order_obj.status) == 0:
                    context['disabled'] = 'none'
                elif user_obj.id == order_obj.userid:
                    context['disabled'] = ''
                if int(order_obj.status) == 0 and order_obj.userid == user_obj.id:
                    context['disabled'] = ''
                if int(order_obj.status) == 5 and order_obj.userid == user_obj.id:
                    context['disabled'] = 'none'

            else:
                if order_obj.status:
                    if int(order_obj.status) == 0:
                        context['openstatus'] = 'active'
                    if int(order_obj.status) == 1:
                        context['confirmstatus'] = 'active'
                    if int(order_obj.status) == 2:
                        context['closestatus'] = 'active'

                if user_obj.id in [int(user.id) for user in order_obj.ordertemp.ccusers.all()] and int(order_obj.status) == 0 and order_obj.ordertemp.is_audit is False:
                    context['confirm'] = True
                if user_obj.id == order_obj.userid and int(order_obj.status) == 1:
                    context['close'] = True
                if user_obj.id == order_obj.userid and int(order_obj.status) == 2:
                    context['reopen'] = True


                if int(order_obj.status) == 2 or int(order_obj.status) == 0:
                    context['disabled'] = 'none'
                elif user_obj.id == order_obj.userid:
                    context['disabled'] = ''


                if int(order_obj.status) == 0 and order_obj.userid == user_obj.id:
                    context['disabled'] = ''
        else:
            self.template_name = 'sysadmin/workorder/list_temp.html'
            self.page_title = u"提交工单"
            temp_type_obj = []
            for i in WorkOrderTypeManager.list(self.request):
                temp_obj = []
                temp = WorkOrderTempManager.filter(self.request,typeid=i.id)
                if temp:
                    for s in temp:
                        temp_obj.append({'name':s.name,'id':s.id})
                    temp_type_obj.append({'isExist':True,'name':i.name,'id':i.id,'temp_obj':temp_obj})
                else:
                    temp_type_obj.append({'name':i.name,'id':i.id,'isExist':False})
            context['temp_type_obj'] = temp_type_obj
        return context