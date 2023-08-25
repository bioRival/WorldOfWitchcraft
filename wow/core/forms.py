from django import forms
from django.db import models
from .models import Post, PostReply


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['category'].label = "Категория"
        self.fields['content'].label = ""

    class Meta:
       model = Post
       fields = [
           'title',
           'category',
           'content',
       ]
       widgets = {
           'title': forms.TextInput(attrs={'class': 'form-control'}),
           'category': forms.Select(attrs={'class': 'form-control'}),
           #'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'вингардиум левиоса...'}),
       }


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""

    class Meta:
       model = PostReply
       fields = [
           'content',
       ]
       widgets = {
           'content': forms.Textarea(attrs={
               'class': 'form-control',
               'placeholder': 'Напишите отклик...',
               'style': 'background-color: #161616; color: #fff; height: 100px',
           }),
       }


class NewsMailForm(forms.Form):
    title = forms.CharField(label= "Заголовок", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label= "Письмо", widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'10'}))

    class Meta:
       fields = [
           'title',
           'content',
       ]