from django.db import models
from django.urls import reverse
from django.utils import timezone
from extensions.utils import jalali_canvert
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
import uuid
import os

# Create your models here.


#Category
class Category(models.Model):
    STATUS_CHOISE = (
        ('p', 'نمایش'),
        ('d', 'پیشنمایش'),
        ('h', 'پنهان'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOISE, verbose_name='وضعیت')
    slug = models.SlugField(max_length=100, unique=True,allow_unicode=True, verbose_name='نامک')
    parent = models.ForeignKey('self', verbose_name= 'دسته پدر', related_name = 'children', null= True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=70, unique=True, verbose_name='سرنام')
    order = models.IntegerField(default=0, verbose_name='چیدمان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'


#Product
class Product(models.Model):
    STATUS_CHOISE = (
        ('p', 'نمایش'),
        ('d', 'پیشنمایش'),
        ('h', 'پنهان'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOISE, verbose_name='وضعیت')
    slug = models.SlugField(unique=True,allow_unicode=True , verbose_name='نامک')
    name = models.CharField(max_length=255, verbose_name="نام")
    description = models.TextField(blank=True, max_length=600, verbose_name='توضیحات')
    review = models.TextField(blank=True, max_length=600, verbose_name='نقد و بررسی')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='images/products/thumbnails/',)
    # images = models.ManyToManyField('Image', blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='دسته')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ نمایش')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    visits = models.PositiveIntegerField(default=0)
    ratings = GenericRelation(Rating, related_query_name='foos')

    class Meta:
        ordering = ['-created']
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'

    def __str__(self):
        return f'{self.id} {self.slug} {self.price}'

    def jCreated(self):
        return jalali_canvert(self.created)
    jCreated.short_description = 'تاریخ ایجاد'

    def visit(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if not Visit.objects.filter(product=self, ip_address=ip_address).exists():
            Visit.objects.create(product=self, ip_address=ip_address)
            self.visits += 1
            self.save()

#
class Visit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='نام محصول')
    ip_address = models.CharField(max_length=255, verbose_name='آی پی آدرس بازدید کننده')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'ip_address')
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدیدها'

    def jCreated_at(self):
        return jalali_canvert(self.created_at)
    jCreated_at.short_description = 'تاریخ بازید'

#Images of Product
class PhotoProduct(models.Model):

    def get_file_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('images/villas/', filename)

    id_product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='photos',
                                 verbose_name='کالا')
    image = models.ImageField(upload_to='images/products/', verbose_name='تصویر کالا')


#Featurs of Product
class FeatureProduct(models.Model):
    id_product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='features',
                                 verbose_name='کالا')
    feature_name = models.CharField(max_length=255, verbose_name ='نام ویژگی')
    feature_value = models.CharField(max_length=255, verbose_name ='مقدار ویژگی')


#Comments of Product
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='کالا')
    name = models.CharField(max_length=255, verbose_name='بازدیدکننده')
    text = models.TextField(verbose_name='پیام')
    replay = models.TextField(null=True, blank=True, verbose_name='پسخ')
    email = models.EmailField(verbose_name='رایانامه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج پیام')
    approved_comment = models.BooleanField(default=False, verbose_name='نمایش پیام')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'


    def jCreated(self):
        return jalali_canvert(self.created)
    jCreated.short_description = 'تاریخ ایجاد'