from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.Form):
    CATEGORIES = {
        ('آموزش', 'آموزش'),
        ('مقاله', 'مقاله'),
        ('خبر', 'خبر'),
        ('پروژه', 'پروژه'),
        ('داستان', 'داستان'),
        ('غیره', 'غیره'),
    }

    title = forms.CharField(max_length = 50, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    body = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}))
    cover = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'http://', 'dir': 'ltr'}))
    short_description = forms.CharField(required = False, empty_value = None, max_length = 156, widget = forms.Textarea(attrs = {'class': 'form-control', 'aria-describedby': 'desc_help', 'rows': '2'}))
    category = forms.CharField(widget = forms.Select(choices = CATEGORIES, attrs = {'class': 'form-control'}))

        
class CommentForm(forms.Form):
    mode = forms.CharField(max_length = 10)
    text = forms.CharField(max_length = 1000)