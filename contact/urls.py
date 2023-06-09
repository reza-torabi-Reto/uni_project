from django.urls import path
from .views import NewMessage

app_name = 'contact'

urlpatterns = [
    path('', NewMessage.as_view(), name='add-message'),
    ]