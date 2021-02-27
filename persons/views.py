from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.core.paginator import Paginator
from main.functions import get_authenticated_user, get_new_notifications
import os

# Models
from main.models import Person, Post, Skill, Notification

# Forms
from .forms import ProfileEditForm, RezomeForm


# Index view
def all_persons(request, page):
    authenticated_user = get_authenticated_user(request)
    persons = Person.objects.all() # Get all persons

    paginate = Paginator(persons, 3)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'persons': paginate.page(page),
        'current_url': str('/user/all/%3Fpage=1/').replace('/', '%2F'),
    }

    return render(request, 'person/list.html', context)


# Users page view
def profile_detail(request, username):
    authenticated_user = get_authenticated_user(request)
    person = get_object_or_404(Person, username=username) # Get Person
    posts = Post.objects.filter(author=person).order_by('-publish_time') # Get the Posts

    paginate = Paginator(posts, 3)
    
    skills_availability = False
    if len(person.skills.all()) > 0:
        skills_availability = True

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
        'posts': paginate.page(1),
        'skills_availability': skills_availability,
        'current_url': str(request.path).replace('/', '%2F'),
    }

    return render(request, 'person/profile/detail.html', context)


# Edit Profile page view
@login_required
def edit_profile(request):
    authenticated_user = get_authenticated_user(request)

    try:
        github_login = request.user.social_auth.get(provider='github')

    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        gitlab_login = request.user.social_auth.get(provider='gitlab')
        
    except UserSocialAuth.DoesNotExist:
        gitlab_login = None

    # If form method == POST
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES) # Get Form

        # If form valid
        if form.is_valid():
            avatar = form.cleaned_data['avatar'] # Read name
            name = form.cleaned_data['name'] # Read name
            public_email = form.cleaned_data['public_email'] # Read public_name
            mobile = form.cleaned_data['mobile'] # Read mobile
            description = form.cleaned_data['description'] # Read description
            year_of_born = form.cleaned_data['year_of_born'] # Read description
            gender = form.cleaned_data['gender'] # Read gender
            work = form.cleaned_data['work']
            skills = form.cleaned_data['skills'] # Read skills
            github = form.cleaned_data['github'] # Read github
            gitlab = form.cleaned_data['gitlab'] # Read gitlab
            stackowerflow = form.cleaned_data['stackowerflow'] # Read stackowerflow
            linkedin = form.cleaned_data['linkedin'] # Read linkedin
            dev = form.cleaned_data['dev'] # Read dev
            website = form.cleaned_data['website'] # Read website

            SKILL_CHOICES = []
            for skill in Skill.objects.all().order_by('name'):
                SKILL_CHOICES.append('_{}_'.format(skill))

            authenticated_user.skills.clear()

            try:
                for skill in SKILL_CHOICES:
                    if skill in skills:
                        authenticated_user.skills.add(Skill.objects.get(name=skill.replace('_', '')))
            except:
                pass

            # Give new data to person
            if avatar is not None:
                if avatar is False:
                    os.remove(authenticated_user.avatar.path)
                    authenticated_user.avatar = None
                    
                else:
                    if authenticated_user.avatar != '':
                        os.remove(authenticated_user.avatar.path)

                    authenticated_user.avatar = avatar

            authenticated_user.name = name
            authenticated_user.public_email = public_email
            authenticated_user.mobile = mobile
            authenticated_user.description = description
            authenticated_user.year_of_born = year_of_born
            authenticated_user.gender = gender
            authenticated_user.work = work
            authenticated_user.github = github
            authenticated_user.gitlab = gitlab
            authenticated_user.stackowerflow = stackowerflow
            authenticated_user.linkedin = linkedin
            authenticated_user.dev = dev
            authenticated_user.website = website
            authenticated_user.save() # Save it
            
            return HttpResponseRedirect('/user/' + authenticated_user.username)
            

    # If form method == GET
    else:
        skills = []
        for skill in authenticated_user.skills.all().order_by('name'):
            skills.append('_{}_'.format(skill))

        # Give form to user
        form = ProfileEditForm(initial = {  
            'avatar': authenticated_user.avatar,
            'name': authenticated_user.name,
            'public_email': authenticated_user.public_email,
            'mobile': authenticated_user.mobile,
            'description': authenticated_user.description,
            'year_of_born': authenticated_user.year_of_born,
            'gender': authenticated_user.gender,
            'work': authenticated_user.work,
            'skills': skills,
            'github': authenticated_user.github,
            'gitlab': authenticated_user.gitlab,
            'stackowerflow': authenticated_user.stackowerflow,
            'linkedin': authenticated_user.linkedin,
            'dev': authenticated_user.dev,
            'website': authenticated_user.website,
        })

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
        'github_login': github_login,
        'gitlab_login': gitlab_login,
    }

    return render(request, 'person/profile/edit.html', context)


# Rezome create view
def rezome_detail(request, username):
    authenticated_user = get_authenticated_user(request)
    person = Person.objects.get(username=username)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'person': person,
    }

    return render(request, 'person/rezome/detail.html', context)


# Rezome create view
@login_required
def edit_rezome(request):
    authenticated_user = get_authenticated_user(request)

    if request.method == 'POST':
        form = RezomeForm(request.POST)

        if form.is_valid():
            rezome = form.cleaned_data['rezome']
            rezome = rezome.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>') # Clean the rezome and recognize line breaks
            

            authenticated_user.rezome = rezome
            authenticated_user.save()

            return HttpResponseRedirect('/user/' + authenticated_user.username + '/rezome/')

    else:
        form = RezomeForm(initial={
            'rezome': authenticated_user.rezome.replace('<br/>', '\n').replace('&lt;', '<').replace('&gt;', '>')
        })

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'form': form,
    }

    return render(request, 'person/rezome/edit.html', context)


# All Notifications
@login_required
def all_notifications(request, page):
    authenticated_user = get_authenticated_user(request)
    notifications = Notification.objects.filter(givver=authenticated_user).order_by('-id')

    paginate = Paginator(notifications, 3)

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'notifications': paginate.page(page),
    }

    return render(request, 'person/notifications/list.html', context)


# Notifications
@login_required
def new_notifications(request):
    authenticated_user = get_authenticated_user(request)
    notifications = Notification.objects.filter(givver=authenticated_user, done=False).order_by('-id')

    for notification in notifications:
        notification.done = True
        notification.save()

    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'notifications': notifications,
    }

    return render(request, 'person/notifications/new.html', context)


# Follow Person view
@login_required
def follow_person(request, username, url):
    authenticated_user = get_authenticated_user(request)
    person = Person.objects.get(username=username)

    if person in authenticated_user.following.all():
        authenticated_user.following.remove(person)
        authenticated_user.len_following = int(authenticated_user.len_following) - 1

        person.followers.remove(authenticated_user)
        person.len_followers = int(person.len_followers) - 1
        

    else:
        authenticated_user.following.add(person)
        authenticated_user.len_following = int(authenticated_user.len_following) + 1

        person.followers.add(authenticated_user)
        person.len_followers = int(person.len_followers) + 1

        notif = Notification(
            givver=person,
            message=f'<a href="/user/{authenticated_user.username}/">{authenticated_user.name}</a> از حالا شما را دنبال می‌کند',
            notif_type='follow'
        )
        notif.save()

    person.save()
    authenticated_user.save()

    return HttpResponseRedirect(url.replace('%2F', '/'))


# Followed Persons view
@login_required
def friends(request, page):
    authenticated_user = get_authenticated_user(request)

    paginate = Paginator(authenticated_user.following.all(), 3)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'persons': paginate.page(page),
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
    }

    return render(request, 'person/friends/list.html', context)


# Followed Persons Posts view
@login_required
def friends_posts(request, page):
    authenticated_user = get_authenticated_user(request)

    posts = []
    all_posts = Post.objects.all().order_by('-publish_time')
    for post in all_posts:
        if post.author in authenticated_user.following.all():
            post.body = post.body.replace('<br/>', ' ')
            posts.append(post)

    paginate = Paginator(posts, 3)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'posts': paginate.page(page),
    }

    return render(request, 'person/friends/posts.html', context)


# Followers view
def followers(request, username, page):
    authenticated_user = get_authenticated_user(request)
    person = Person.objects.get(username=username)

    followers_available = False
    if len(person.followers.all()) > 0:
        followers_available = True

    paginate = Paginator(person.followers.all(), 3)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'persons': paginate.page(page),
        'person': person,
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
        'followers_available': followers_available,
    }

    return render(request, 'person/followers.html', context)


# Followers view
def followings(request, username, page):
    authenticated_user = get_authenticated_user(request)
    person = Person.objects.get(username=username)

    following_available = False
    if len(person.following.all()) > 0:
        following_available = True

    paginate = Paginator(person.following.all(), 3)
            
    context = {
        'authenticated_user': authenticated_user,
        'new_notifications': get_new_notifications(authenticated_user),
        'persons': paginate.page(page),
        'person': person,
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
        'following_available': following_available,
    }

    return render(request, 'person/followings.html', context)
