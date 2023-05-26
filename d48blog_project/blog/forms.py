from django.contrib.auth.models import User
from dataclasses import field
from django import forms
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)
    

from blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')


class Signupform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
        