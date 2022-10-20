from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect


def chart_list(request):
    return render(request, "chart_list.html")


def chart_bar(request):
    legend = ["11", "22"]
    data_list = [
        {
            "name": "11",
            "type": "bar",
            "data": [15, 20, 36, 10, 10, 100]
        },
        {
            "name": "22",
            "type": "bar",
            "data": [45, 10, 66, 40, 20, 10]
        }
    ]
    date_list = ["1m", "2m", "3m", "4m", "5m"]
    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': data_list,
            'x_axis': date_list
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {"value": 2048, "name": 'IT部门'},
        {"value": 1735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ["上海", "广西"]
    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '广西',
            "type": 'line',
            "stack": 'Total',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    """ highcharts示例 """

    return render(request, 'highcharts.html')
