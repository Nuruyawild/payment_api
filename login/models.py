from django.db import models

# Create your models here.


class User(models.Model):
    gender=(
        ('male','男'),
        ('femal','女'),
    )

    name=models.CharField(max_length=128,unique=True)
    password=models.CharField(max_length=256)
    email=models.EmailField(unique=True)
    balance=models.IntegerField(default=0)
    order_id=models.IntegerField(default=1)
    realname=models.CharField(max_length=256)
    user_id_number=models.IntegerField(default=0)
    user_phone=models.IntegerField(default=0)

    sex=models.CharField(max_length=32,choices=gender,default='男')
    c_time=models.DateTimeField(auto_now_add=True)

    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering=["-c_time"]
        verbose_name = "user"
        verbose_name_plural = "user"

class invoice_detail(models.Model):
    orderid=models.IntegerField(default=1)
    AID=models.IntegerField(default=1)
    totalAmount=models.IntegerField(default=0)
    airline=models.CharField(max_length=50)
    key=models.CharField(max_length=100, default='')


class ConfirmString(models.Model):

    code = models.CharField(max_length=256)

    user = models.OneToOneField('User', on_delete=models.CASCADE)

    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "confirm"
        verbose_name_plural = "confirm"