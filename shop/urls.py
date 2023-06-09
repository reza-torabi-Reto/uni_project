from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('products-category/<slug:slug>/', products_category, name='products-category'),
    path('products/<slug:slug>/', products, name='products'),
    path('products-list', products_list, name='products-list'),
    path('product/<slug:slug>/', product, name='product'),
    path('search/', search, name='search'),
    path('faq/', faq, name='faq'),
    path('about/', about, name='about'),

]