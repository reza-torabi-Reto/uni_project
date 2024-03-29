# Generated by Django 4.1.2 on 2023-04-28 06:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'نمایش'), ('d', 'پیشنمایش'), ('h', 'پنهان')], max_length=1, verbose_name='وضعیت')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='نامک')),
                ('title', models.CharField(max_length=70, unique=True, verbose_name='سرنام')),
                ('order', models.IntegerField(default=0, verbose_name='چیدمان')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category', verbose_name='دسته پدر')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'نمایش'), ('d', 'پیشنمایش'), ('h', 'پنهان')], max_length=1, verbose_name='وضعیت')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='نامک')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=600, verbose_name='توضیحات')),
                ('review', models.TextField(blank=True, max_length=600, verbose_name='نقد و بررسی')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thumbnail', models.ImageField(upload_to='images/products/thumbnails/')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ نمایش')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='دسته')),
            ],
            options={
                'ordering': ['-price'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('email', models.EmailField(max_length=254, verbose_name='رایانامه')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج پیام')),
                ('approved_comment', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='shop.review')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products/', verbose_name='تصویر کالا')),
                ('id_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='shop.product', verbose_name='کالا')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=255, verbose_name='نام ویژگی')),
                ('feature_value', models.CharField(max_length=255, verbose_name='مقدار ویژگی')),
                ('id_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='shop.product', verbose_name='کالا')),
            ],
        ),
    ]
