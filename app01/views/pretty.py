from app01 import models

from django.shortcuts import HttpResponse, render, redirect

from app01.utils.pagination import Pagination
from app01.utils.form import PrettyModelForm, PrettyEditModelForm


def pretty_list(request):
    # form = PrettyNumMod:leForm()
    data_dict = {}
    mobile = request.GET.get('mobile', '')
    if mobile:
        data_dict["mobile__contains"] = mobile
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset, page_size=10)
    # 根据用户想要访问的页码，计算出起止位置
    # page = int(request.GET.get("page", 1))

    # form = models.PrettyNum.objects.filter(**data_dict).order_by("id")[page_object.start:page_object.end]
    # form = models.PrettyNum.objects.all().order_by("-level")
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"form": page_queryset, "search_data": mobile, "page_string": page_string}
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    if request.method == "GET":
        pretty_data = PrettyModelForm()
        return render(request, "change.html", {"form": pretty_data,
                                               "title": "添加靓号",
                                               "way": "user"})
    pretty_data = PrettyModelForm(data=request.POST)
    context = {"form": pretty_data,
               "title": "添加靓号",
               "way": "pretty"}
    if pretty_data.is_valid():
        pretty_data.save()
        return redirect("/pretty/list/")
    else:
        return render(request, "change.html", context)


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    else:
        return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request):
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
