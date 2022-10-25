from django.db import models
import time, datetime
from django.core.validators import RegexValidator


class Admin(models.Model):
    """管理员"""
    username = models.CharField(max_length=32, verbose_name="管理员账号")
    password = models.CharField(max_length=32, verbose_name="管理员密码")


class Department(models.Model):
    """部门"""
    title = models.CharField(max_length=32, verbose_name="部门标题")

    # depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # depart是对象，输出对象时，通过__str__(self)定制显示内容，（重写call方法
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工信息"""
    name = models.CharField(max_length=64, verbose_name="员工姓名")
    password = models.CharField(max_length=64, verbose_name="员工密码")
    age = models.IntegerField(verbose_name="员工年龄")
    account = models.DecimalField(verbose_name="账号余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")  # DateTimeField
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)
    # 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE,
                               default="质量管理中心")
    """" # 置空
    depart = models.ForeignKey(to="Department", to_field="id", null=True,  blank=True, on_delete=models.SET_NULL)
   """

    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    """靓号"""
    mobile = models.CharField(verbose_name="手机号",
                              max_length=32)  # ,validators=[RegexValidator(r'^1[3-9]\d(10)$', '数字必须1开头且是11位数')]
    price = models.IntegerField(verbose_name="价格", null=True, blank=True)
    level_choices = ((1, "一级"), (2, "二级"), (3, "三级"), (4, "四级"), (5, "五级"))
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)
    status_choices = ((1, "未占用"), (2, "已占用"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Task(models.Model):
    """任务"""
    title = models.CharField(verbose_name="任务名称", max_length=64)
    detail = models.TextField(verbose_name="任务详情")
    level_choice = (
        (1, "非常紧急"), (2, "紧急"), (3, "一般"), (4, "轻微")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    user = models.ForeignKey(verbose_name="负责人", to=UserInfo, on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="订单名称", max_length=32)
    price = models.IntegerField(verbose_name="订单价格")
    status_choice = ((1, "待支付"), (2, "已支付"))
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choice, default=1)
    user = models.ForeignKey(verbose_name="用户名", to=UserInfo, on_delete=models.CASCADE)


class OrderInfo(models.Model):
    """ 另外一个订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="订单名称", max_length=32)
    price = models.IntegerField(verbose_name="订单价格")
    status_choice = ((1, "待支付"), (2, "已支付"))
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="用户名", to=Admin, on_delete=models.CASCADE)


class Boss(models.Model):
    """老板"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """城市"""
    name = models.CharField(verbose_name="城市", max_length=32)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')