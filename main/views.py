# THE CODE IS CLEAN

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from main.functions import mskf
from random import choice

# Models
from main.models import Person,\
                        Post,\
                        Ad


# Index view
def index(request):
    if request.user.is_authenticated:

        # If user has Person model
        try:
            # Load the user's person model
            user = Person.objects.get(username=request.user.username)

        # If user doesnt has Person model
        except:
            # Create a new Person model for user
            user = Person(
                username=request.user.username,
                name=request.user.first_name)
            user.save()

            # Redirect user to "wellcome" page
            return HttpResponseRedirect('/wellcome/')

    # Redirect user to index's first page
    return HttpResponseRedirect('%3Fpage=1/')


# Posts page view
def posts(request, page):
    # Try to load authenticated user
    try:
        person = get_object_or_404(Person, username=request.user.username)

    except:
        person = None

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
        'person': person,
        'posts': paginate.page(page),
        'ad': ad,
    }

    # Add authenticated user and it's new notifications to context
    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    # Show "index" page template to user
    return render(request, 'index.html', context)


# Wellcome page view
def wellcome(request):
    context = {}

    # Add authenticated user and it's new notifications to context
    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    # Show "wellcome" page template to user
    return render(request, 'wellcome.html', context)
