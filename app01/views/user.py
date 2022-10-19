from django.shortcuts import HttpResponse, redirect, render
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    """用户列表"""
    data_dict = {}
    name = request.GET.get("name", "")
    if name:
        data_dict["name__contains"] = name
    queryset = models.UserInfo.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "data_list": page_object.page_queryset,
        "search_data": name,
        "page_string": page_object.html()
    }
    # for item in data_list:
    #     create_time = item.create_time.strftime("%Y-%m-%d")
    #     gender_text = item.get_gender_display()
    #     depart = item.depart.title
    #     print(create_time, gender_text, depart)
    return render(request, "user_list.html", context)


def user_edit(request, nid):
    """编辑用户"""
    if request.method == "GET":
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form})


def user_delete(request):
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {"form": form,
                                               "title": "添加用户",
                                               "way": "user"})
    form = UserModelForm(data=request.POST)
    context = {"form": form,
               "title": "添加用户",
               "way": "user"}
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "change.html", context)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
            "title": "添加用户",
            "way": "user"
        }
        return render(request, "user_add.html", context)
    user_data = UserModelForm(data=request.POST)
    context = {"user_data": user_data,
               "title": "添加用户",
               "way": "user"}
    if user_data.is_valid():
        user_data.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_add.html", context)
