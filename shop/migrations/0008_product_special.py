# Generated by Django 4.1.2 on 2023-06-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special',
            field=models.IntegerField(default=0, verbose_name='تخفیف'),
        ),
    ]
