from app01 import models

from django.shortcuts import render, HttpResponse, redirect

from app01.utils.form import CityModelForm
from app01.utils.pagination import Pagination


def city_list(request):
    if request.method == "GET":
        form_list = CityModelForm()
        data_dict = {}
        cid = request.GET.get('id', '')
        if cid:
            data_dict["cid__contains"] = cid
        queryset = models.City.objects.filter(**data_dict).order_by("-id")
        page_object = Pagination(request, queryset)
        page_queryset = page_object.page_queryset
        page_string = page_object.html()
        context = {
            "form_list": form_list,
            "form_data": page_queryset,
            "search_data": cid,
            "page_string": page_string
        }
        return render(request, "city_list.html", context)
    form = CityModelForm(request.POST)


def city_add(request):
    title = "添加城市"
    if request.method == "GET":
        form = CityModelForm()
        return render(request, "upload_model_form.html", {"form": form, "title": title})
    form = CityModelForm(request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_model_form.html", {"form": form, "title": title})
