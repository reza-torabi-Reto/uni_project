from django.shortcuts import render
from .models import Message
from .forms import AddMessageForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.

class NewMessage(SuccessMessageMixin, CreateView):
    model = Message
    form_class = AddMessageForm
    template_name = 'contact/new-message.html'
    success_url = reverse_lazy('contact:add-message')

    success_message = 'پیام شما با موفقیت ثبت شد'
#
# def add_message(request):
#     if request.method == 'POST':
#         message_form = AddMessageForm(request.POST)
#         if message_form.is_valid():
#             message_form.save()
#             new_c = 'ok'
#
#         return render(request, "contact/new-message.html", {'ok':new_c})
#     else:
#         message_form = AddMessageForm()
#         return render(request, "contact/new-message.html", {'message_form': message_form})