import json, random
from datetime import datetime

from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import OrderInfoModelForm


def order_list(request):
    form_list = OrderInfoModelForm()
    # print(form_list)
    data_dict = {}
    oid = request.GET.get("oid", "")
    if oid:
        data_dict["oid__contains"] = oid
    queryset = models.OrderInfo.objects.filter(**data_dict).order_by('-id')

    page_object = Pagination(request, queryset, page_size=10)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        "form_list": form_list,
        "form_data": page_queryset,
        "search_data": oid,
        "page_string": page_string
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    form = OrderInfoModelForm(data=request.POST)
    print("-------------------")
    print(form)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def order_delete(request):
    uid = request.GET.get("uid")
    exists = models.OrderInfo.objects.filter(id=uid).exists()
    if not exists:
        return HttpResponse(json.dumps({"status": False, "error": "删除失败"}))
    models.OrderInfo.objects.filter(id=uid).delete()
    return HttpResponse(json.dumps({"status": True}))


@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    print("-------------------")
    print(uid)
    row_object = models.OrderInfo.objects.filter(id=uid).first()
    if not row_object:
        return HttpResponse(json.dumps({"status": False, "tips": "编辑失败"}))

    form = OrderInfoModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return HttpResponse(json.dumps({"status": True}))

    return HttpResponse(json.dumps({"status": False, "error": form.errors}))


def order_detail(request):
    # """ 方法一 """
    # uid = request.GET.get("uid")
    # row_object = models.OrderInfo.objects.filter(id=uid).first()
    # if not row_object:
    #     return HttpResponse(json.dumps({"status": False, "error": "数据不存在"}))
    # result = {
    #     "title": row_object.title,
    #     "price": row_object.price,
    #     "status": row_object.status
    # }
    # return HttpResponse(json.dumps("data": result))

    """ 方法二 """
    uid = request.GET.get("uid")

    result = models.OrderInfo.objects.filter(id=uid).values("title", "price", "status").first()
    if not result:
        return HttpResponse(json.dumps({"status": False, "error": "数据不存在"}))
    return HttpResponse(json.dumps({"status": True, "data": result}))
