"""mypractice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import depart, user, pretty, admin, account, task, order, chart, upload

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/multi/', depart.depart_multi),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/delete/', user.user_delete),

    # 靓号管理
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/delete/', pretty.pretty_delete),

    # 管理员
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录注销
    path('logout/', account.logout),
    path('login/', account.login),
    path('image/code/', account.image_code),

    # 任务
    path('task/add/', task.task_add),
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/delete/', task.task_delete),


    # 订单
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/edit/', order.order_edit),
    path('order/detail/', order.order_detail),

    # 图表
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/line/', chart.chart_line),
    path('chart/pie/', chart.chart_pie),
    path('chart/highcharts/', chart.highcharts),

    # 文件
    path('upload/list/', upload.upload_list),
]
