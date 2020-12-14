from django import forms
from django.core.exceptions import ValidationError
import re


class ProfileEditForm(forms.Form):
    GENDER_CHOICES = (
        ('مرد', 'مرد'),
        ('زن', 'زن'),
    )
    
    PROGRAMMING_CHOICES = (
        ('_C_', 'C'),
        ('_C++_', 'C++'),
        ('_C#_', 'C#'),
        ('_Objective-C_', 'Objective-C'),
        ('_Java_', 'Java'),
        ('_JavaScript_', 'JavaScript'),
        ('_Python_', 'Python'),
        ('_PHP_', 'PHP'),
        ('_HTML_', 'HTML'),
        ('_CSS_', 'CSS'),
        ('_Perl_', 'Perl'),
        ('_Swift_', 'Swift'),
        ('_Kotlin_', 'Kotlin'),
        ('_Go_', 'Go'),
        ('_Ruby_', 'Ruby'),
        ('_Basic_', 'Basic'),
        ('_Pascal_', 'Pascal'),
        ('_Lua_', 'Lua'),
        ('_R_', 'R'),
        ('_Rust_', 'Rust'),
        ('_TypeScript_', 'TypeScript'),
    )

    YEARS = [(None, 'هیچکدام')]

    for year in range(1330, 1395):
        YEARS.append((str(year), str(year)),)

    YEARS = tuple(YEARS)

    WORK_CHOICES = (
        (None, 'هیچکدام'),
        ('طراح وب - فرانت‌اند', 'طراح وب - فرانت‌اند'),
        ('برنامه نویس وب - بک‌اند', 'برنامه نویس وب - بک‌اند'),
        ('برنامه نویس فول استک', 'برنامه نویس فول استک'),
        ('برنامه نویس دسکتاپ', 'برنامه نویس دسکتاپ'),
        ('برنامه نویس موبایل', 'برنامه نویس موبایل'),
        ('برنامه نویس سیستم', 'برنامه نویس سیستم'),
        ('برنامه نویس سخت افزار', 'برنامه نویس سخت افزار'),
        ('برنامه نویس بازی', 'برنامه نویس بازی'),
        ('مدیر سیستم', 'مدیر سیستم'),
        ('امنیت سیستم', 'امنیت سیستم'),
    )

    avatar = forms.ImageField(required = False)
    name = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class': 'form-control'}))
    public_email = forms.EmailField(max_length = 200, required = False, empty_value = None, widget = forms.EmailInput(attrs = {'class': 'form-control', 'placeholder': 'email@example.com', 'dir': 'ltr'}))
    mobile = forms.CharField(max_length = 11, min_length = 11, required = False, empty_value = None, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '09123456789'}))
    description = forms.CharField(max_length = 200, required = False, empty_value = None, widget = forms.Textarea(attrs = {'class': 'form-control', 'rows': '2'}))
    year_of_born = forms.CharField(widget = forms.Select(choices = YEARS, attrs = {'class': 'form-control'}), required = False, empty_value = None)
    gender = forms.CharField(widget = forms.RadioSelect(choices = GENDER_CHOICES, attrs = {'class': 'form-check form-check-inline form-check-input'}), required = False, empty_value = None)
    work = forms.CharField(widget = forms.Select(choices = WORK_CHOICES, attrs = {'class': 'form-control'}), required = False, empty_value = None)
    programming = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = PROGRAMMING_CHOICES, attrs = {'class': ''}), required = False, empty_value = None)
    github = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'https://github.com/', 'dir': 'ltr'}))
    gitlab = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'https://gitlab.com/', 'dir': 'ltr'}))
    stackowerflow = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'https://stackoverflow.com/', 'dir': 'ltr'}))
    linkedin = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'https://www.linkedin.com/', 'dir': 'ltr'}))
    dev = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'https://dev.to/', 'dir': 'ltr'}))
    website = forms.URLField(required = False, empty_value = None, widget = forms.URLInput(attrs = {'class': 'form-control', 'placeholder': 'http://', 'dir': 'ltr'}))

    def clean_github(self):
        data = self.cleaned_data['github']

        if data is not None:
            if re.match('^http://github.com/|https://github.com/', data):
                return data

            raise ValidationError('فرمت وارد شده نادرست است.')

    def clean_gitlab(self):
        data = self.cleaned_data['gitlab']

        if data is not None:
            if re.match('^http://gitlab.com/|https://gitlab.com/', data):
                return data

            raise ValidationError('فرمت وارد شده نادرست است.')

    def clean_stackowerflow(self):
        data = self.cleaned_data['stackowerflow']
    
        if data is not None:
            if re.match('^http://stackoverflow.com/|https://stackoverflow.com/', data):
                return data

            raise ValidationError('فرمت وارد شده نادرست است.')

    def clean_linkedin(self):
        data = self.cleaned_data['linkedin']
        
        if data is not None:
            if re.match('^http://linkedin.com/|https://linkedin.com/|http://www.linkedin.com/|https://www.linkedin.com/', data):
                return data

            raise ValidationError('فرمت وارد شده نادرست است.')

    def clean_dev(self):
        data = self.cleaned_data['dev']

        if data is not None:
            if re.match('^http://dev.to/|https://dev.to/', data):
                return data

            raise ValidationError('فرمت وارد شده نادرست است.')


class RezomeForm(forms.Form):
    rezome = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}), required = False, empty_value = "")
