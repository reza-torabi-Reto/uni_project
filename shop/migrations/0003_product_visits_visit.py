# Generated by Django 4.1.2 on 2023-05-04 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'unique_together': {('product', 'ip_address')},
            },
        ),
    ]
