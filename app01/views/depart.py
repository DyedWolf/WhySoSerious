from app01 import models
from app01.utils.pagination import Pagination

from django.shortcuts import render, redirect
from app01.utils.form import DepartModelForm


def depart_list(request):
    """部门列表"""
    data_dict = {}
    title = request.GET.get("title", "")
    if title:
        data_dict["title__contains"] = title
    queryset = models.Department.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)
    context = {"data_list": page_object.page_queryset, "page_string": page_object.html(), "search_data": title}
    return render(request, "depart_list.html", context)


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        form = DepartModelForm()
        return render(request, "change.html", {"form": form, "title": "添加部门",
                                               "way": "depart"})
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/depart/list/")
    context = {"form": form,
               "title": "添加部门",
               "way": "depart"}
    return render(request, "change.html", context)


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """编辑部门"""
    title = models.Department.objects.filter(id=nid).first()
    # print(title.id, title.title)
    if request.method == "GET":
        return render(request, "depart_edit.html", {"title": title.title})
    if request.method == "POST":
        new_title = request.POST.get("title")
        models.Department.objects.filter(id=nid).update(title=new_title)
        return redirect("/depart/list/")
