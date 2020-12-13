# THE CODE IS CLEAN

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from main.functions import mskf

# Models
from main.models import Person

# Forms
from .forms import SignUpForm


# Sign up view
def signup(request):
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

            # Create a Person model for user
            person = Person(
                username=username,
                name=username)
            person.save()

            # Login current user
            login(request, user)

            # Redirect user to "wellcome" page
            return HttpResponseRedirect('/wellcome/')

    # If form method == GET
    else:
        form = SignUpForm() # Give form to user

    context = {
        'form': form,
    }

    # Add authenticated user and it's new notifications to context
    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    # Show "signup" page template to user
    return render(request, 'registration/signup.html', context)