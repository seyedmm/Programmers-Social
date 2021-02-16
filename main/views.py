# THE CODE IS CLEAN

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications
from random import choice

# Models
from main.models import Person, Post, Ad


# Index view
def index(request):
    authenticated_user = get_authenticated_user(request)

    # Load all posts order by there publish time
    posts = Post.objects.all().order_by('-publish_time')
    paginate = Paginator(posts, 3) # Paginate by 3

    # Load banner
    try:
        ad = Ad.objects.filter(type='صفحه اول')
        ad = choice(ad)

        while ad.available_views == '0':
            ad.delete()
            ad = choice(Ad.objects.filter(type='صفحه اول'))

        ad.available_views = int(ad.available_views) - 1
        ad.save()

    except:
        ad = None

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'posts': paginate.page(1),
        'ad': ad,
    }
    
    # Show "index" page template to user
    return render(request, 'index/index.html', context)


# Posts page view
def posts(request, page):
    authenticated_user = get_authenticated_user(request)

    # Load all posts order by there publish time
    posts = Post.objects.all().order_by('-publish_time')
    paginate = Paginator(posts, 3) # Paginate by 3

    # Load banner
    try:
        ad = Ad.objects.filter(type='صفحه اول')
        ad = choice(ad)

        while ad.available_views == '0':
            ad.delete()
            ad = choice(Ad.objects.filter(type='صفحه اول'))

        ad.available_views = int(ad.available_views) - 1
        ad.save()

    except:
        ad = None

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'posts': paginate.page(page),
        'ad': ad,
    }

    # Show "index" page template to user
    return render(request, 'index/index.html', context)


# Wellcome page view
def wellcome(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show "wellcome" page template to user
    return render(request, 'pages/wellcome.html', context)


# Support page view
def support(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show "supprot" page template to user
    return render(request, 'pages/support.html', context)


# Rocket page view
def rocket(request):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show "rocket" page template to user
    return render(request, 'pages/rocket.html', context)


def page_not_found_view(request, exception=None):
    authenticated_user = get_authenticated_user(request)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
    }

    # Show template
    return render(request, 'admin/404.html', context)
