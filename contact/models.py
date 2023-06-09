from django.db import models
from django.core.validators import RegexValidator
from extensions.utils import jalali_canvert
# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=70, verbose_name='نام')
    text = models.TextField(verbose_name='پیام')
    email = models.EmailField(verbose_name='رایانامه')
    phone = models.CharField(max_length=12, verbose_name='شماره تماس',
        validators=[RegexValidator(regex='^[0-9]', message="برای درج شماره تماس لطفا فقط عدد وارد کنید"),],)
    is_ready = models.BooleanField(default=False, verbose_name='خوانده شده')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج پیام')

    def __str__(self):
        return self.name


    def jCreated(self):
        return jalali_canvert(self.created)
    jCreated.short_description = 'تاریخ ایجاد'

    class Meta:
        verbose_name = 'بخش پیام ها'
        verbose_name_plural = 'بخش پیام ها'

