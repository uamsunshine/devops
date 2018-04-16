# -*- coding=utf-8 -*-
import logging,json
from collections import defaultdict
from django.template import defaultfilters as filters
from django.core.urlresolvers import reverse, reverse_lazy
from horizon import tables
from omg_dashboard.api.sysadmin.workorder import (
    WorkOrderManager,
    WorkOrderFieldManager,
    WorkOrderFieldTypeManager,
    WorkOrderTypeManager,
    WorkOrderTempManager
    )
from omg_dashboard.dashboards.sysadmin.models import WorkOrderField,WORK_ORDER_STATUS
from omg_auth.manager import UserManager
from omg_dashboard.utils.functions import safe_decode,safe_encode
from omg_dashboard.utils import functions as omg_func


LOG = logging.getLogger(__name__)






class WorkOrderField(tables.LinkAction):
    name = "workorderfield"
    verbose_name = u'工单字段'
    url = "horizon:sysadmin:workorder:field"
    # classes = ("ajax-modal",)
    icon = "list-ul"
    policy_rules = ["sysadmin.workorder.field"]

class WorkOrderEfficiency(tables.LinkAction):
    name = "workorderefficiency"
    verbose_name = u'工单效率'
    url = "horizon:sysadmin:workorder:efficiency"
    # classes = ("ajax-modal",)
    icon = "dashboard"
    policy_rules = ["sysadmin.workorder.efficiency"]


class UpdateField(tables.LinkAction):
    name = u"updatefield"
    verbose_name = u"修改字段"
    url = "horizon:sysadmin:workorder:updatefield"
    #classes = ("ajax-modal", )
    policy_rules = ["sysadmin.workorder.updatefield"]

class DeleteField(tables.DeleteAction):
    help_text = "删除字段后,无法恢复"
    verbose_name = u"删除字段"
    policy_rules = ["sysadmin.workorder.deletefield"]

    @staticmethod
    def action_present(count):
        return (u"删除", u"删除", count)

    @staticmethod
    def action_past(count):
        return (u"删除", u"删除", count)

    def delete(self, request, obj_id):
        WorkOrderFieldManager.delete(obj_id)

    def allowed(self,request,datum):
        if WorkOrderTempManager.filter(request,fieldid=datum.id):
            return False
        else:
            return True


class FieldType(tables.LinkAction):
    name = "fieldtype"
    verbose_name = u'添加字段'
    url = "horizon:sysadmin:workorder:fieldtype"
    icon = "plus"
    policy_rules = ["sysadmin.workorder.fieldtype"]


class CreateFieldType(tables.LinkAction):
    name = "createfieldtype"
    verbose_name = u'增加'
    url = "horizon:sysadmin:workorder:createfieldtype"
    icon = "plus"
    policy_rules = ["sysadmin.workorder.createfieldtype"]


class ReplyWorkOrder(tables.LinkAction):
    name = u'listworkorder'
    verbose_name = u'返回' 
    url = "horizon:sysadmin:workorder:index"
    icon = 'reply'
    policy_rules = []


class ReplyWorkOrderField(tables.LinkAction):
    name = u'listworkorder'
    verbose_name = u'返回' 
    url = "horizon:sysadmin:workorder:field"
    icon = 'reply'
    policy_rules = []


class ReplyWorkOrderTemp(tables.LinkAction):
    name = u'listworkorder'
    verbose_name = u'返回' 
    url = "horizon:sysadmin:workorder:workordertemp"
    icon = 'reply'
    policy_rules = []


class WorkOrderTemp(tables.LinkAction):
    name = "workordertemp"
    verbose_name = u'工单模板'
    url = "horizon:sysadmin:workorder:workordertemp"
    #classes = ("ajax-modal",)
    icon = "list-ul"
    policy_rules = ["sysadmin.workorder.workordertemp"]


class UpdateTemp(tables.LinkAction):
    name = u"updatetemp"
    verbose_name = u"修改模板"
    url = "horizon:sysadmin:workorder:updatetemp"
    #classes = ("ajax-modal", )
    policy_rules = ["sysadmin.workorder.updatetemp"]

class DeleteTemp(tables.DeleteAction):
    help_text = "删除模板后,无法恢复"
    verbose_name = u"删除模板"
    policy_rules = ["sysadmin.workorder.deletetemp"]

    @staticmethod
    def action_present(count):
        return (u"删除", u"删除", count)

    @staticmethod
    def action_past(count):
        return (u"删除", u"删除", count)

    def delete(self, request, obj_id):
        WorkOrderTempManager.delete(obj_id)

    def allowed(self,request,datum):
        if WorkOrderManager.list(request,ordertemp=datum.id):
            return False
        else:
            return True


class WorkOrderType(tables.LinkAction):
    name = "workordertemp"
    verbose_name = u'模板类型'
    url = "horizon:sysadmin:workorder:temptype"
    icon = "list-ul"
    policy_rules = ["sysadmin.workorder.temptype"]


class ListTemp(tables.LinkAction):
    name = "listtemp"
    verbose_name = u'提交工单'
    url = "horizon:sysadmin:workorder:listtemp"
    icon = "plus"
    policy_rules = []


class ListOrder(tables.LinkAction):
    name = "listorder"
    verbose_name = u'查看'
    url = "horizon:sysadmin:workorder:listorder"
    icon = "plus"
    policy_rules = [""]


class EditOrder(tables.LinkAction):
    name = "editorder"
    verbose_name = u'编辑'
    url = "horizon:sysadmin:workorder:editorder"
    icon = "plus"
    policy_rules = ["sysadmin.workorder.editorder"]

    def allowed(self,request,datum):
        if WorkOrderManager.get(request,id=datum.id).ordertemp.is_audit:
            return True
        else:
            return False

class CreateTempType(tables.LinkAction):
    name = "createtemptype"
    verbose_name = u'新建模板类型'
    url = "horizon:sysadmin:workorder:createtemptype"
    # classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ["sysadmin.workorder.createtemptype"]


class CreateTemp(tables.LinkAction):
    name = "createtemp"
    verbose_name = u'新建模板'
    url = "horizon:sysadmin:workorder:createtemp"
    icon = "plus"
    policy_rules = ["sysadmin.workorder.createtemp"]


class UpdateTempType(tables.LinkAction):
    name = "updatetemptype"
    verbose_name = u'编辑'
    url = "horizon:sysadmin:workorder:updatetemptype"
    # classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ["sysadmin.workorder.updatetemptype"]


class DeleteTempType(tables.DeleteAction):
    help_text = "删除模板类型后,无法恢复"
    verbose_name = u"删除模板类型"
    policy_rules = ["sysadmin.workorder.deletetemptype"]

    @staticmethod
    def action_present(count):
        return (u"删除", u"删除", count)

    @staticmethod
    def action_past(count):
        return (u"删除", u"删除", count)

    def delete(self, request, obj_id):
        WorkOrderTypeManager.delete(obj_id)

    def allowed(self,request,datum):
        if WorkOrderTempManager.filter(request,typeid=datum.id):
            return False
        else:
            return True

class DeleteOrder(tables.DeleteAction):
    help_text = "删除工单后,无法恢复"
    verbose_name = u"删除工单"
    policy_rules = ["sysadmin.workorder.deleteorder"]

    @staticmethod
    def action_present(count):
        return (u"删除", u"删除", count)

    @staticmethod
    def action_past(count):
        return (u"删除", u"删除", count)

    def delete(self, request, obj_id):
        WorkOrderManager.delete(obj_id)

    def allowed(self,request,datum):
        if UserManager.get(id=request.user.id).is_superuser is True:
            return True
        else:
            return False


class CreateOrder(tables.LinkAction):
    name = "createorder"
    verbose_name = u'提交工单'
    url = "horizon:sysadmin:workorder:createorder"
    icon = "plus"
    policy_rules = ["sysadmin.workorder.createorder"]



class OrderFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('userid', u"提交人", True),
                      ('confirmuser', u"处理人", True),
                      ('status',u'工单状态',True),
                      ('ordernum',u'工单ID',True),
                      ('name',u'工单模板',True),
                     )



class OrderTempFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('name', u"模板名", True),
                      ('description', u"模板描述", True),
                     )


class OrderFieldFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('name', u"字段名称", True),
                      ('description', u"字段描述", True),
                      ('fieldtype',u'字段类型',True),
                     )


class WorkOrderTable(tables.DataTable):
    # hidestatus = tables.Column("hidestatus", verbose_name=u"隐藏状态")
    orderid = tables.Column("id", verbose_name=u"工单ID")
    confirmuser = tables.Column(lambda obj: WorkOrderManager.get_handlinguser(obj),verbose_name=u'处理人')
    userid = tables.Column(lambda obj: UserManager.get(id=obj.userid).username if obj.userid else '',verbose_name=u'提交人')
    # cc = tables.Column(lambda obj:' | '.join([ UserManager.get(id=i).username for i in json.loads(obj.ordertemp.cc)]) if json.loads(obj.ordertemp.cc) else '',verbose_name=u'抄送')
    # sendTo = tables.Column(lambda obj: ' | '.join([ UserManager.get(id=i).username for i in json.loads(obj.ordertemp.default_send)]) if json.loads(obj.ordertemp.default_send) else '',verbose_name=u'发送')
    name = tables.Column(lambda obj:obj.ordertemp.name, verbose_name=u'工单模板')
    typename = tables.Column(lambda obj: obj.ordertemp.typeid.name, verbose_name=u'工单类型')
    # ordernum = tables.Column("ordernum", verbose_name=u"工单编号")
    status = tables.Column(lambda obj: WorkOrderManager.get_status(obj.status),verbose_name=u'工单状态')
    # priority = tables.Column(lambda obj:WorkOrderManager.get_priority(obj.priority),verbose_name=u'优先级')
    addedtime = tables.Column('addedtime',verbose_name=u'提交时间')
    confirmtime = tables.Column('confirmtime',verbose_name=u'确认时间')
    dealtime = tables.Column(lambda obj:omg_func.formate_second_date(int(obj.dealtime)) if obj.dealtime else '',verbose_name=u'处理时间')
    # dealtime = tables.Column(lambda obj:omg_func.formate_second_date(int(obj.dealtime)) if obj.dealtime else '',verbose_name=u'处理时间')

    class Meta(object):
        name = "workorder"
        verbose_name = u'工单'
        pagination_param = "page"
        prev_pagination_param = "page"
        multi_select = False
        table_actions = (OrderFilterAction,WorkOrderEfficiency,WorkOrderField,WorkOrderTemp,ListTemp,)
        row_actions = (ListOrder,EditOrder,DeleteOrder,)


class WorkOrderFieldTable(tables.DataTable):
    name = tables.Column('name',verbose_name=u'字段名称')
    fieldtype = tables.Column(lambda obj: obj.fieldtype.name,verbose_name=u'字段类型')
    value = tables.Column(lambda obj:  " | ".join([ i['name'].encode('utf-8') for i in json.loads(obj.value)]) if type(json.loads(obj.value)) is list  else json.loads(obj.value) ,verbose_name=u'字段类型值')
    description = tables.Column('description',verbose_name=u'字段描述')

    class Meta(object):
        name = "workorderfield"
        verbose_name = u'工单字段'
        pagination_param = 'page'
        prev_pagination_param = 'page'
        multi_select = False
        table_actions = (OrderFieldFilterAction,ReplyWorkOrder,FieldType,)
        row_actions = (UpdateField,DeleteField,)


class WorkOrderFieldTypeTable(tables.DataTable):
    name = tables.Column('name',verbose_name=u'字段类型名')
    description = tables.Column('description',verbose_name=u'字段类型描述')

    class Meta(object):
        name = "workorderfieldtype"
        verbose_name = u'工单字段类型'
        pagination_param = "page"
        prev_pagination_param = "page"
        multi_select = False
        table_actions = (ReplyWorkOrderField,)
        row_actions=(CreateFieldType,)


class WorkOrderTempTable(tables.DataTable):
    name = tables.Column("name",verbose_name=u"模板名")
    description = tables.Column('description',verbose_name=u'模板描述')
    addedtime = tables.Column('addedtime',verbose_name=u'添加时间')

    class Meta(object):
        name = 'workordertemp'
        verbose_name = u'模板'
        pagination_param = 'page'
        prev_pagination_param = 'page'
        multi_select = False
        table_actions = (OrderTempFilterAction,ReplyWorkOrder,WorkOrderType,CreateTemp)
        row_actions = (UpdateTemp,DeleteTemp,)


class ListTempTable(tables.DataTable):
    name = tables.Column("name",verbose_name=u"工单类型")
    description = tables.Column('description',verbose_name=u'描述')

    class Meta(object):
        name = 'listtemp'
        verbose_name = u'列出模板'
        pagination_param = 'page'
        prev_pagination_param = 'page'
        multi_select = False
        table_actions = (ReplyWorkOrder,)
        row_actions = (CreateOrder,)


class WorkOrderTempTypeTable(tables.DataTable):
    name = tables.Column("name",verbose_name=u"模板类型名")
    addedtime = tables.Column('addedtime',verbose_name=u'添加时间')

    class Meta(object):
        name = 'temptype'
        verbose_name = u'模板类型'
        pagination_param = 'page'
        prev_pagination_param = 'page'
        multi_select = False
        table_actions = (ReplyWorkOrderTemp,CreateTempType)
        row_actions = (UpdateTempType,DeleteTempType,)


class CreateFieldTempTable(tables.LinkAction):
    name = "createfieldtemp"
    verbose_name = u'字段模板'
    url = "horizon:sysadmin:workorder:createfieldtemp"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ["sysadmin.workorder.createfieldtemp"]
