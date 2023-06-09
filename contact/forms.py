from django import forms
from .models import Message


class AddMessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddMessageForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'نامتان را بنویسی'
        self.fields['email'].widget.attrs['placeholder'] = 'رایانامه خود را وارد کنید'
        self.fields['phone'].widget.attrs['placeholder'] = 'شماره تماس خود را وارد کنید'
        self.fields['text'].widget.attrs['placeholder'] = 'پیام خود را بنویسید'

    class Meta:
        fields = ['name', 'text', 'email', 'phone']
        model = Message


