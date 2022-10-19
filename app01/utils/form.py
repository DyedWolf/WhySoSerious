from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.enctypt import md5
from django import forms
from django.core.validators import ValidationError


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # exclude = ["level] # 排除 level


class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # exclude = ["level] # 排除 level

    def clean_mobile(self):
        """验证输入字段"""
        txt_mobile = self.cleaned_data["mobile"]

        # 当前编辑的那一行的id
        # self.instance.pk
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()

        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


class DepartModelForm(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = ["title"]

    def clean_title(self):
        txt_title = self.cleaned_data["title"]
        exists = models.Department.objects.exclude(id=self.instance.pk).filter(title=txt_title).exists()

        if len(txt_title) < 2:
            raise ValidationError("格式错误")
        if exists:
            raise ValidationError("部门已存在")
        return txt_title


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(
            username=self.cleaned_data["username"]).exists()
        if confirm_password != password:
            raise ValidationError("密码不一致")
        if exists:
            raise ValidationError("管理员已存在")
        return confirm_password


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能修改成重复密码")
        return md5_pwd

    def clean_confirm_password(self):
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        # exists = models.Admin.objects.exclude(id=self.instance.pk).filter(
        #     username=self.cleaned_data["username"]).exists()
        if confirm_password != password:
            raise ValidationError("密码不一致")
        # if exists:
        #     raise ValidationError("管理员已存在")
        return confirm_password


# class LoginModelForm(BootStrapModelForm):
#     class Meta:
#         model = models.Admin
#         fields = ["username", "password"]
#
#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         if not password:
#             raise ValidationError("请输入密码")
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if not username:
#             raise ValidationError("请输入账号")


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid", "user"]


class OrderInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.OrderInfo
        exclude = ['oid', 'admin']
