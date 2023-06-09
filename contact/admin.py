from django.contrib import admin
from .models import Message

@admin.register(Message)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'jCreated', 'is_ready']
    filds = ['name', 'phone', 'email','text', 'jCreated', 'is_ready']
    list_filter = ('is_ready',)
    search_fields = ('name', 'text', 'email', 'phone')
    save_on_top = True
    list_per_page = 10
