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
    PROGRAMMING_CHOICES = (
        ('C', 'C'),
        ('C++', 'C++'),
        ('C#', 'C#'),
        ('Objective-C', 'Objective-C'),
        ('Java_', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('Python', 'Python'),
        ('PHP', 'PHP'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('Perl', 'Perl'),
        ('Swift', 'Swift'),
        ('Kotlin', 'Kotlin'),
        ('Go', 'Go'),
        ('Ruby', 'Ruby'),
        ('Basic', 'Basic'),
        ('Pascal', 'Pascal'),
        ('Lua', 'Lua'),
        ('R', 'R'),
        ('Rust', 'Rust'),
        ('TypeScript', 'TypeScript'),
    )
    LICENSE_CHOICES = (
        ('None', 'None'),
        ('Apache License 2.0', 'Apache License 2.0'),
        ('GNU General Public License v3.0', 'GNU General Public License v3.0'),
        ('MIT License', 'MIT License'),
        ('BSD 2-Clause "Simplified" License', 'BSD 2-Clause "Simplified" License'),
        ('BSD 3-Clause "New" or "Revised" License', 'BSD 3-Clause "New" or "Revised" License'),
        ('Boost Software License 1.0', 'Boost Software License 1.0'),
        ('Creative Commons Zero v1.0 Universal', 'Creative Commons Zero v1.0 Universal'),
        ('Eclipse Public License 2.0', 'Eclipse Public License 2.0'),
        ('GNU Affero General Public License v3.0', 'GNU Affero General Public License v3.0'),
        ('GNU General Public License v2.0', 'GNU General Public License v2.0'),
        ('GNU Lesser General Public License v2.1', 'GNU Lesser General Public License v2.1'),
        ('Mozilla Public License 2.0', 'Mozilla Public License 2.0'),
        ('The Unlicense', 'The Unlicense'),
    )

    title = forms.CharField(max_length = 50, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    body = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}))
    cover = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'http://', 'dir': 'ltr'}))
    short_description = forms.CharField(required = False, empty_value = None, max_length = 156, widget = forms.Textarea(attrs = {'class': 'form-control', 'aria-describedby': 'desc_help', 'rows': '2'}))
    category = forms.CharField(widget = forms.Select(choices = CATEGORIES, attrs = {'class': 'form-control'}))

        
class CommentForm(forms.Form):
    mode = forms.CharField(max_length = 10)
    text = forms.CharField(max_length = 1000)