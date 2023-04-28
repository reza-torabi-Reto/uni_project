from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products-category/<slug:slug>/', views.products_category, name='products-category'),
    path('products/<slug:slug>/', views.products, name='products'),
    path('products-list', views.products_list, name='products-list'),
    path('product/<slug:slug>/', views.product, name='product'),

]