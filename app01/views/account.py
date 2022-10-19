from django import forms
from io import BytesIO

from django.shortcuts import HttpResponse, render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.enctypt import md5
from app01.utils.code import check_code


# """ 第一种没继承 """
# class LoginForm(forms.Form):
#     username = forms.CharField(label="用户名", widget=forms.TextInput)
#     password = forms.CharField(label="密码", widget=forms.PasswordInput)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             if field.widget.attrs:
#                 field.widget.attrs["class"] = "form-control"
#                 field.widget.attrs["placeholder"] = field.label
#             else:
#                 field.widget.attrs = {
#                     "class": "form-control",
#                     "placeholder": field.label
#                 }

class LoginForm(BootStrapForm):
    """ 第二种用了 bootstrap继承 """
    username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        # form = LoginModelForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("code_string", "")
        print(user_input_code, code)
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")
    return render(request, "login.html", {"form": form})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """ 生成图片验证码 """
    img, code_string = check_code()
    request.session["code_string"] = code_string
    request.session.set_expiry(60)
    steam = BytesIO()
    img.save(steam, 'png')

    return HttpResponse(steam.getvalue())
