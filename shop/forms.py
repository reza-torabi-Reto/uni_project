from django import forms
from .models import *

class CommentForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('name', 'text', 'email')

# class ReplyForm(forms.ModelForm):
#
#     class Meta:
#         model = Review
#         fields = ('author', 'text',)