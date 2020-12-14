# THE CODE IS CLEAN

from django import forms
from django.core.exceptions import ValidationError


# File upload form
class FileUploadForm(forms.Form):
    image = forms.ImageField()
    compress = forms.BooleanField()

    # Check the image size
    def clean_image(self):
        data = self.cleaned_data['image']

        if data.size > 10000000:
            raise ValidationError('حجم فایل نباید از 10 مگابایت بیشتر باشد!')

        return data
