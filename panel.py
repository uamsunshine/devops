# -*- coding=utf-8 -*-
import horizon
from omg_dashboard.dashboards.sysadmin import dashboard


class workorder(horizon.Panel):
    name = u"工单系统"
    slug = "workorder"
    permissions = []

dashboard.Admin.register(workorder)