# Generated by Django 4.1.2 on 2023-05-05 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_visit_options_alter_visit_ip_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created'], 'verbose_name': 'کالا', 'verbose_name_plural': 'کالاها'},
        ),
    ]