# THE CODE IS CLEAN

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from main.functions import get_authenticated_user, get_new_notifications

# Models
from main.models import Person

# Forms
from .forms import SignUpForm


# Sign up view
def signup(request):
    authenticated_user = get_authenticated_user(request)

    if authenticated_user != None:
        return HttpResponseRedirect('/')

    # If form method == POST
    if request.method == 'POST':
        form = SignUpForm(request.POST) # Get Form

        # If form valid
        if form.is_valid():
            username = form.cleaned_data['username'] # Read username

            # Create a user with form data
            user = form.save(commit=False)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()

            # Login current user
            login(request, user)

            # Redirect user to "wellcome" page
            return HttpResponseRedirect('/wellcome/')

    # If form method == GET
    else:
        form = SignUpForm() # Give form to user

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
    }

    # Show "signup" page template to user
    return render(request, 'registration/signup.html', context)
