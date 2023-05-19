from django.contrib import admin
from .models import *
admin.site.site_header = 'پنل مدیریت'


def publish(self, request, queryset):
    queryset.update(approved_comment= True)


publish.short_description = "نمایش انتخاب شده ها"


def hide(self, request, queryset):
    queryset.update(approved_comment= False)


hide.short_description = "پنهان کردن انتخاب شده ها"


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
    fields = ['category','name', 'slug', 'visits','status', 'price', 'description', 'review', 'thumbnail']
    list_display = ['name', 'slug', 'jCreated']
    save_on_top = True
    readonly_fields= ['visits',]
    list_per_page = 10
    inlines = [ProductImageAdmin, FeatureProductAdmin,]


class ReviewAdmin(admin.ModelAdmin):
    fields = ['created',  'product', 'name', 'text', 'replay', 'approved_comment']
    list_display = ['name','jCreated', 'approved_comment', 'product']
    readonly_fields = ['created',  'product' , 'name']
    actions = [publish, hide]



class VisitAdmin(admin.ModelAdmin):
    fields = [ 'ip_address','product', 'created_at']
    list_display = ['ip_address','product',  'jCreated_at']
    # readonly_fields = ['created',  'product' , 'name']
    actions = [publish, hide]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Visit, VisitAdmin)
