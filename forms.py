# -*- coding=utf8 -*-
from django.conf import settings
from django.core import validators
from django.forms import ValidationError
from django.forms.widgets import HiddenInput
from django.template import defaultfilters
from horizon import exceptions, forms, messages
from omg_dashboard.api.sysadmin.workorder import WorkOrderTypeManager,WorkOrderTempManager
from omg_dashboard.api.sysadmin.workorder import WorkOrderManager,WorkOrderFieldManager,WorkOrderFieldTypeManager
from omg_auth.manager import UserManager,UserGroupManager
import logging

LOG = logging.getLogger(__name__)



class CreateTempTypeForm(forms.SelfHandlingForm):
    name = forms.CharField(
        label=u'模板类型名',
        required=True,
    )

    icon = forms.ChoiceField(
        label=u'模板样式',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'form-control chosen-select-no-results',
                'data-placeholder': u'模板样式',
            }),
        required=True,
        )

    description = forms.CharField(
        label=u'模板类型描述',
        required=False,
        )

    def __init__(self, request, *args, **kwargs):
        super(CreateTempTypeForm, self).__init__(request, *args, **kwargs)
        list_icon = [(0,u'重点蓝'),(1,u'成功绿'),(2,u'信息蓝'),(3,u'警告黄'),(4,u'危险红'),(5,u'默认灰')]
        self.fields['icon'].choices = list_icon 

    def clean(self):
        data = super(CreateTempTypeForm, self).clean()
        name = data.get('name',None)
        obj = WorkOrderTypeManager.filter(name=name)
        if name is None:
            raise ValidationError(u'模板类型名不能为空')
        elif obj:
            raise ValidationError(u'类型名称已经存在')
        else:
            return data

    def handle(self, request, data):
        try:
            WorkOrderTypeManager.add(request,name=data['name'],icon=data['icon'],description=data['description'])
            messages.success(request, u'新建成功')
        except Exception, e:
            messages.error(request, e.message)
            return False
        return True


class UpdateTempTypeForm(forms.SelfHandlingForm):
    name = forms.CharField(
        label=u'模板类型名',
        required=True,
    )

    icon = forms.ChoiceField(
        label=u'模板样式',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'form-control chosen-select-no-results',
                'data-placeholder': u'模板样式',
            }),
        required=True,
        )

    description = forms.CharField(
        label=u'模板类型描述',
        required=False,
        )


    def __init__(self, request, *args, **kwargs):
        super(UpdateTempTypeForm, self).__init__(request, *args, **kwargs)
        self.initial = kwargs['initial']
        self.fields['name'].initial = self.initial['name']
        list_icon = [(0,u'重点蓝'),(1,u'成功绿'),(2,u'信息蓝'),(3,u'警告黄'),(4,u'危险红'),(5,u'默认灰')]
        self.fields['icon'].choices = list_icon 

    def clean(self):
        data = super(UpdateTempTypeForm, self).clean()
        name = data.get('name',None)
        typeid = self.request.resolver_match.kwargs['id']        
        obj = WorkOrderTypeManager.exclude(typeid=typeid,name=name)        
        if name is None:
            raise ValidationError(u'模板类型名不能为空')
        elif obj:
            raise ValidationError(u'类型名称已经存在')
        else:
            return data

    def handle(self, request, data):
        typeid = request.resolver_match.kwargs['id']
        try:
            WorkOrderTypeManager.update(request,typeid=typeid,name=data['name'],icon=data['icon'],description=data['description'])
            messages.success(request, u'更新成功')
        except Exception, e:
            messages.error(request, e.message)
            return False
        return True


class CreateTempForm(forms.SelfHandlingForm):
    name = forms.CharField(
        label=u'模板名',
        required=True,
        error_messages={'required':u'模板名不能为空',}
    )

    description = forms.CharField(
        label=u'模板描述',
        required=False,
    )

    temptype = forms.ChoiceField(label=u'模板类型',
        choices=(),
    )

    field = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'字段',
            }), 
        choices = (),
        label=u'字段', 
        required=True,
        error_messages={'required':u'字段不能为空',}
        )

    auditgroup = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'审核组',
            }), 
        choices = (),
        label=u'审核人', 
        required=False,
    )

    tousers = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'确认人',
            }), 
        choices = (),
        label=u'确认人', 
        required=False,
        error_messages={'required':u'确认人不能为空',}
    )

    cc = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'处理人',
            }), 
        choices = (),
        label=u'处理人', 
        required=True,
        error_messages={'required':u'处理人不能为空',}
    )

    is_audit = forms.ChoiceField(
            label=u'是否审核',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    is_cc = forms.ChoiceField(
            label=u'是否抄送',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    is_attachment = forms.ChoiceField(
            label=u'是否添加附件',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True,
        )

    is_confirm = forms.ChoiceField(
            label=u'是否确认',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    def __init__(self, request, *args, **kwargs):
        super(CreateTempForm, self).__init__(request, *args, **kwargs)
        list_temp_type = [(obj.id,obj.name) for obj in WorkOrderTypeManager.list(request)]
        list_field = [(obj.id,obj.name) for obj in WorkOrderFieldManager.list(request) ]
        list_user = [(obj['id'],obj['username']) for obj in UserManager.list()]
        list_user_group = [(obj.id,obj.name) for obj in UserGroupManager.list() ]
        self.fields['temptype'].choices = list_temp_type 
        self.fields['field'].choices = list_field
        self.fields['auditgroup'].choices = list_user_group
        self.fields['cc'].choices = list_user
        self.fields['tousers'].choices = list_user

    def clean(self):
        data = super(CreateTempForm, self).clean()
        name = data.get('name',None)
        temptype = data.get('temptype',None)
        field = self.request.POST.getlist('field')
        data['field'] = field
        auditgroup = self.request.POST.getlist('auditgroup')
        data['auditgroup'] = auditgroup
        tousers = self.request.POST.getlist('tousers')
        data['tousers'] = tousers
        cc = self.request.POST.getlist('cc')
        data['cc'] = cc
        obj = WorkOrderTempManager.filter(self.request,name=name)

        if name is None:
            raise ValidationError(u'模板类型名不能为空')
        elif temptype is None:
            raise ValidationError(u'模板类型不能为空')
        elif field is None:
            raise ValidationError(u'字段不能为空')
        elif cc is None:
            raise ValidationError(u'默认抄送不能为空')
        elif obj:
            raise ValidationError(u'模板名已经存在')
        else:
            return data

    def handle(self, request, data):
        name = data['name']
        description = data.get('description',None)
        try:
            temptype = WorkOrderTypeManager.get(id=data['temptype'])
        except Exception:
            temptype = ''
        field = data['field']
        cc = data['cc']
        auditgroup = data['auditgroup']
        args = {
            'name':name,
            'description':description,
            'typeid':temptype,
            'is_audit':int(data['is_audit']),
            'is_cc':int(data['is_cc']),
            'is_attachment':int(data['is_attachment']),
            'is_confirm':int(data['is_confirm']),
            }
        try:
            objects = WorkOrderTempManager.add(request,**args)
            for group in auditgroup:
                try:
                    groupobj = UserGroupManager.get(id=group)
                    objects.auditgroup.add(groupobj)
                except Exception:
                    pass
            for user in cc:
                try:
                    userobj = UserManager.get(id=user)
                    objects.ccusers.add(userobj)
                except Exception:
                    pass
            for user in data['tousers']:
                try:
                    userobj = UserManager.get(id=user)
                    objects.ccusers.add(userobj)
                except Exception:
                    pass
            for field in data['field']:
                try:
                    fieldobj = WorkOrderFieldManager.get('',fieldid=field)
                    objects.fieldid.add(fieldobj)
                except Exception:
                    pass
            messages.success(request, u'更新成功')
        except Exception, e:
            messages.error(request, e.message)
            return False
        return True

class UpdateTempForm(forms.SelfHandlingForm):

    name = forms.CharField(
        label=u'模板名',
        required=True,
        error_messages={'required':u'模板名不能为空',}
    )

    description = forms.CharField(
        label=u'模板描述',
        required=False,
    )

    temptype = forms.ChoiceField(label=u'模板类型',
        choices=(),
    )

    field = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'字段',
            }), 
        choices = (),
        label=u'字段', 
        required=True,
        error_messages={'required':u'字段不能为空',}
        )

    auditgroup = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'审核组',
            }), 
        choices = (),
        label=u'审核人', 
        required=False,
        error_messages={'required':u'审核组不能为空',}
    )

    tousers = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'确认人',
            }), 
        choices = (),
        label=u'确认人', 
        required=False,
        error_messages={'required':u'确认人不能为空',}
    )

    cc = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'处理人',
            }), 
        choices = (),
        label=u'处理人', 
        required=True,
        error_messages={'required':u'处理人不能为空',}
    )

    is_audit = forms.ChoiceField(
            label=u'是否审核',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),
            required=True
            )

    is_cc = forms.ChoiceField(
            label=u'是否抄送',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    is_attachment = forms.ChoiceField(
            label=u'是否添加附件',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    is_confirm = forms.ChoiceField(
            label=u'是否确认',widget=forms.RadioSelect,
            choices=(((1,u'是'),(0,u'否'))),required=True
        )

    def __init__(self, request, *args, **kwargs):
        super(UpdateTempForm, self).__init__(request, *args, **kwargs)
        list_temp_type = [(obj.id,obj.name) for obj in WorkOrderTypeManager.list(request)]
        list_field = [(obj.id,obj.name) for obj in WorkOrderFieldManager.list(request) ]
        list_user = [(obj['id'],obj['username']) for obj in UserManager.list()]
        list_user_group = [(obj.id,obj.name) for obj in UserGroupManager.list()]
        self.fields['temptype'].choices = list_temp_type 
        self.fields['field'].choices = list_field
        self.fields['auditgroup'].choices = list_user_group
        self.fields['cc'].choices = list_user
        self.fields['tousers'].choices = list_user

    def clean(self):
        data = super(UpdateTempForm, self).clean()
        name = data.get('name',None)
        temptype = data.get('temptype',None)
        field = self.request.POST.getlist('field')
        data['field'] = field
        auditgroup = self.request.POST.getlist('auditgroup')
        data['auditgroup'] = auditgroup
        tousers = self.request.POST.getlist('tousers')
        data['tousers'] = tousers
        cc = self.request.POST.getlist('cc')
        data['cc'] = cc
        tempid = self.request.resolver_match.kwargs['id']   
        obj = WorkOrderTempManager.exclude(self.request,tempid=tempid,name=name)

        if name is None:
            raise ValidationError(u'模板类型名不能为空')
        elif temptype is None:
            raise ValidationError(u'模板类型不能为空')
        elif field is None:
            raise ValidationError(u'字段不能为空')
        elif cc is None:
            raise ValidationError(u'默认抄送不能为空')
        elif obj:
            raise ValidationError(u'模板名已经存在')
        else:
            return data

    def handle(self, request, data):
        name = data['name']
        description = data.get('description',None)
        temptype = data['temptype']
        fields = data['field']
        cc = data['cc']
        auditgroup = data['auditgroup']
        tempid = request.resolver_match.kwargs['id']
        try:
            temptype = WorkOrderTypeManager.get(id=data['temptype'])
        except Exception:
            temptype = ''
        args = {
            'name':name,
            'typeid':temptype,
            'description':description,
            'is_audit':int(data['is_audit']),
            'is_cc':int(data['is_cc']),
            'is_attachment':int(data['is_attachment']),
            'is_confirm':int(data['is_confirm']),
            }
        try:
            objects = WorkOrderTempManager.update(request,tempid,**args)
            tempobj = WorkOrderTempManager.get('',id=tempid)
            for item in tempobj.auditgroup.all():
                tempobj.auditgroup.remove(item)
            for group in auditgroup:
                tempobj.auditgroup.add(group)
            for item in tempobj.tousers.all():
                tempobj.tousers.remove(item)
            for user in data['tousers']:
                tempobj.tousers.add(user)
            for item in tempobj.ccusers.all():
                tempobj.ccusers.remove(item)
            for user in cc:
                tempobj.ccusers.add(user)
            for item in tempobj.fieldid.all():
              tempobj.fieldid.remove(item)
            for field in fields:
              tempobj.fieldid.add(field)
            messages.success(request, u'更新成功')
            return True
        except Exception, e:
            messages.error(request, e.message)
            return False


class OrderUpdateForm(forms.SelfHandlingForm):


    audituser = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'审核人',
            }), 
        choices = (),
        label=u'审核人', 
        required=False,
        error_messages={'required':u'审核人不能为空',}
    )

    cc = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class':'chosen-select-no-results',
                'data-placeholder': u'抄送人',
            }), 
        choices = (),
        label=u'抄送人', 
        required=False,
        error_messages={'required':u'处理人不能为空',}
    )


    def __init__(self, request, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(request, *args, **kwargs)
        list_user = [(obj['id'],obj['username']) for obj in UserManager.list()]
        self.fields['audituser'].choices = list_user
        self.fields['cc'].choices = list_user

    def clean(self):
        data = super(OrderUpdateForm, self).clean()
        audituser = self.request.POST.getlist('audituser')
        data['audituser'] = audituser
        cc = self.request.POST.getlist('cc')
        data['cc'] = cc

    def handle(self, request, data):
        cc = data['cc']
        audituser = data['audituser']
        orderid = request.resolver_match.kwargs['id']
        try:
            objects = WorkOrderManager.get('',id=orderid)
            if objects:
                for user in objects.ccusers.all():
                    objects.ccusers.remove(user)
                for user in objects.auditusers.all():
                    objects.auditusers.remove(user)
                for user in cc:
                    objects.ccusers.add(user)
                for user in audituser:
                    objects.auditusers.add(user)
                messages.success(request, u'更新成功')
                return True
        except Exception, e:
            messages.error(request, e.message)
            return False
