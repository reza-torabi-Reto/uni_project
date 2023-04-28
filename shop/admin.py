from django.contrib import admin
from .models import *

admin.site.site_header = 'پنل مدیریت'


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'parent', 'status', 'order']
    list_display = ['title', 'slug',]
    save_on_top = True
    list_per_page = 10


class ProductImageAdmin(admin.StackedInline):
    model = PhotoProduct

class FeatureProductAdmin(admin.StackedInline):
    model = FeatureProduct


class ProductAdmin(admin.ModelAdmin):
    fields = ['category','name', 'slug', 'status', 'price', 'description', 'review', 'thumbnail']
    list_display = ['name', 'slug',]
    save_on_top = True
    list_per_page = 10
    inlines = [ProductImageAdmin, FeatureProductAdmin]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
