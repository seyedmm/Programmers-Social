# THE CODE IS CLEAN

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications, compress_image
from django.core.exceptions import ValidationError
import os

# Models
from main.models import Person, Cloud, File

# Forms
from .forms import FileUploadForm


# Cloud Index view
@login_required
def cloud_index(request):
    authenticated_user = get_authenticated_user(request)
    cloud = Cloud.objects.get(owner=authenticated_user)

    # Get user's cloud uploaded files
    files = File.objects.filter(cloud=cloud).order_by('-id')

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'cloud': cloud,
        'files': files,
    }

    # Show "cloud index" page template to user
    return render(request, 'cloud/cloud_index.html', context)


# Upload file view
@login_required
def upload_file(request):
    authenticated_user = get_authenticated_user(request)
    cloud = Cloud.objects.get(owner=authenticated_user)

    # If request method == POST
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        # If form valid
        if form.is_valid():
            image = form.cleaned_data['image']
            compress = form.cleaned_data['compress']

            file = File(
                cloud=cloud,
                file=image)
            file.save()

            # If user want to compress the image
            if compress is True:
                compress_image(file.file.path)

            # calculate file size
            filesize = file.file.size / 1000
            if filesize < 100:
                filesize = 0.1

            elif filesize < 200:
                filesize = 0.2

            elif filesize < 300:
                filesize = 0.3

            elif filesize < 400:
                filesize = 0.4

            elif filesize < 500:
                filesize = 0.5

            elif filesize < 600:
                filesize = 0.6

            elif filesize < 700:
                filesize = 0.7

            elif filesize < 800:
                filesize = 0.8

            elif filesize < 900:
                filesize = 0.9

            else:
                filesize = round(filesize / 100) / 10

            # Calculate cloud's used space
            cloud.used_space = float(cloud.used_space)
            cloud.used_space = round((cloud.used_space + filesize) * 10) / 10
            cloud.used_percent = round(
                float(cloud.used_space) * 1000 / float(cloud.space)) / 10
            cloud.save()

            # Redirect user to "cloud" page
            return HttpResponseRedirect('/cloud/')

    # If request method == GET
    else:
        form = FileUploadForm() # Give the form to user

    # Check cloud's available space
    available_space = float(cloud.space) - float(cloud.used_space)
    if available_space >= 10.0:
        available_space = True

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
        'cloud': cloud,
        'available_space': available_space,
    }

    # Show "upload file" page template to user
    return render(request, 'cloud/upload_file.html', context)
