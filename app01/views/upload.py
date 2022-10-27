import os

from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect

from app01 import models
from app01.utils.form import UpForm, UpModelForm, CityModelForm


def upload_list(request):
    """文件操作例子"""
    if request.method == 'GET':
        return render(request, "upload_list.html")
    # print(request.FILES)
    # {'avatar': [<InMemoryUploadedFile: ABD337FD-6095-4208-A273-689499A6F808.jpeg (image/jpeg)>]}>
    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("...")


def upload_form(request):
    """Form上传文件和数据"""
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取图片内容，写入到文件路径
        image_object = form.cleaned_data.get("img")
        # file_path = "app01/static/img/{}".format(image_object.name)
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name) settings.MEDIA_ROOT 绝对路径
        media_path = os.path.join('media', image_object.name)
        f = open(media_path, mode="wb")
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        models.Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=media_path,
        )
        return render(request, "upload_form.html", {"form": form, "title": title})


def upload_modal_form(request):
    """上传文件和数据"""
    title = "ModelForm上传文件和数据"
    if request.method == "GET":
        form = CityModelForm()
        return render(request, "upload_model_form.html", {"form": form, "title": title})
    form = CityModelForm(request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/upload/model/form/")
    return render(request, "upload_model_form.html", {"form": form, "title": title})
