import json
from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination


@csrf_exempt
def task_add(request):
    # print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def task_list(request):
    form_list = TaskModelForm()

    data_dict = {}
    task_id = request.GET.get("task_id", "")
    if task_id:
        data_dict["task_id__contains"] = task_id
    queryset = models.Task.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset, page_size=10)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"form_data": page_queryset, "form_list": form_list, "search_data": task_id, "page_string": page_string}

    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    data_dict = {"status": True, "data": [request.POST.get("name"), request.POST.get("age")]}

    return HttpResponse(json.dumps(data_dict))


def task_delete(request):
    nid = request.GET.get("nid")
    models.Task.objects.filter(id=nid).delete()
    return redirect('/task/list/')
