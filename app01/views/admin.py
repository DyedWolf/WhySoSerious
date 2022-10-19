from app01 import models
from app01.utils.pagination import Pagination
from django.shortcuts import HttpResponse, render, redirect
from app01.utils.form import AdminModelForm, AdminResetModelForm


def admin_list(request):
    """管理员列表"""
    data_dict = {}
    username = request.GET.get("username", "")
    if username:
        data_dict["username__contains"] = username
    queryset = models.Admin.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)
    context = {"data_list": page_object.page_queryset,
               "page_string": page_object.html(),
               "search_data": username
               }
    return render(request, "admin_list.html", context)


def admin_add(request):
    """管理员添加"""
    if request.method == 'GET':
        form = AdminModelForm()
        render(request, "admin_add.html", {"form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    context = {"form": form,
               "title": "添加管理员",
               "way": "admin"}
    return render(request, "change.html", context)


def admin_delete(request):
    nid = request.GET.get("nid")
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_edit(request, nid):
    """ 编辑管理员 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, "error.html", {"error_txt": "数据不存在"})
        redirect("/admin/list/")
    if request.method == "GET":
        form = AdminModelForm(instance=row_object)
        return render(request, "admin_edit.html", {"form": form})
    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "admin_edit.html", {"form": form})


def admin_reset(request, nid):
    """ 重置密码 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})
