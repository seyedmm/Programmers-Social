from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.core.paginator import Paginator
from main.functions import mskf

# Models
from main.models import Person,\
                        Post,\
                        Programming,\
                        Notification

# Forms
from .forms import ProfileEditForm,\
                   RezomeForm


# Index view
def all_persons(request, page):
    if request.user.is_authenticated:
        try:
            user = Person.objects.get(username = request.user.username)

        except:
            user = Person(username = request.user.username, name = request.user.first_name)
            user.save()
    
    else:
        user = None
    
    persons = Person.objects.all() # Get all persons

    paginate = Paginator(persons, 3)

    context = {
        'persons': paginate.page(page),
        'current_url': str('/user/all/%3Fpage=1/').replace('/', '%2F'),
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'all_persons.html', context)


# Users page view
def profile_detail(request, username):
    person = get_object_or_404(Person, username = username) # Get Person
    
    programming_availability = False
    if len(person.programming.all()) > 0:
        programming_availability = True

    posts = Post.objects.filter(author = person) # Get Persons posts
    count_posts = [post.title for post in posts]
    post_availability = False

    if len(count_posts) > 0:
        post_availability = True

    context = {
        'person': person,
        'posts': posts,
        'post_availability': post_availability,
        'programming_availability': programming_availability,
        'current_url': str(request.path).replace('/', '%2F'),
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'profile_detail.html', context)


# Edit Profile page view
@login_required
def edit_profile(request):
    person = Person.objects.get(username = request.user.username) # Get the Person

    try:
        github_login = request.user.social_auth.get(provider = 'github')

    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        gitlab_login = request.user.social_auth.get(provider = 'gitlab')
        
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
            programming = form.cleaned_data['programming'] # Read programming
            github = form.cleaned_data['github'] # Read github
            gitlab = form.cleaned_data['gitlab'] # Read gitlab
            stackowerflow = form.cleaned_data['stackowerflow'] # Read stackowerflow
            linkedin = form.cleaned_data['linkedin'] # Read linkedin
            dev = form.cleaned_data['dev'] # Read dev
            website = form.cleaned_data['website'] # Read website

            PROGRAMMING_CHOICES = {
                '_C_': 'C', 
                '_C++_': 'C++',
                '_C#_': 'C#',
                '_Objective-C_': 'Objective-C',
                '_Java_': 'Java',
                '_JavaScript_': 'JavaScript',
                '_Python_': 'Python',
                '_PHP_': 'PHP', 
                '_HTML_': 'HTML',
                '_CSS_': 'CSS', 
                '_Perl_': 'Perl',
                '_Swift_': 'Swift',
                '_Kotlin_': 'Kotlin',
                '_Go_': 'Go',
                '_Ruby_': 'Ruby',
                '_Basic_': 'Basic',
                '_Pascal_': 'Pascal', 
                '_Lua_': 'Lua',
                '_R_': 'R',
                '_Rust_': 'Rust',
                '_TypeScript_': 'TypeScript',
            }

            person.programming.clear()
            try:
                for p_lang in PROGRAMMING_CHOICES:
                    if p_lang in programming:
                        programming_language = Programming.objects.get(language = PROGRAMMING_CHOICES[p_lang])
                        person.programming.add(programming_language)
            except:
                pass

            # Give new data to person
            if avatar != None:
                if avatar == False:
                    person.avatar = None
                    
                else:
                    person.avatar = avatar

            person.name = name
            person.public_email = public_email
            person.mobile = mobile
            person.description = description
            person.year_of_born = year_of_born
            person.gender = gender
            person.work = work
            person.github = github
            person.gitlab = gitlab
            person.stackowerflow = stackowerflow
            person.linkedin = linkedin
            person.dev = dev
            person.website = website
            person.save() # Save it
            
            return HttpResponseRedirect('/user/' + person.username)
            

    # If form method == GET
    else:
        p_langs = []
        for p_lang in person.programming.all():
            p_langs.append('_{}_'.format(p_lang))

        # Give form to user
        form = ProfileEditForm(initial = {  
                                            'avatar': person.avatar,
                                            'name': person.name,
                                            'public_email': person.public_email,
                                            'mobile': person.mobile,
                                            'description': person.description,
                                            'year_of_born': person.year_of_born,
                                            'gender': person.gender,
                                            'work': person.work,
                                            'programming': p_langs,
                                            'github': person.github,
                                            'gitlab': person.gitlab,
                                            'stackowerflow': person.stackowerflow,
                                            'linkedin': person.linkedin,
                                            'dev': person.dev,
                                            'website': person.website,
                                          })

    context = {
        'form': form,
        'github_login': github_login,
        'gitlab_login': gitlab_login,
        'person': person,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'edit_profile.html', context)


# Rezome create view
def rezome_detail(request, username):
    person = Person.objects.get(username = username)

    context = {
        'person': person,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'rezome_detail.html', context)


# Rezome create view
@login_required
def edit_rezome(request):
    person = Person.objects.get(username = request.user.username)

    if request.method == 'POST':
        form = RezomeForm(request.POST)

        if form.is_valid():
            rezome = form.cleaned_data['rezome']
            rezome = rezome.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>') # Clean the rezome and recognize line breaks
            

            person.rezome = rezome
            person.save()

            return HttpResponseRedirect('/user/' + person.username + '/rezome/')

    else:
        form = RezomeForm(initial = {'rezome': person.rezome.replace('<br/>', '\n').replace('&lt;', '<').replace('&gt;', '>')})

    context = {
        'form': form,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'edit_rezome.html', context)


# All Notifications
@login_required
def all_notifications(request, page):
    person = Person.objects.get(username = request.user.username)
    notifications = Notification.objects.filter(givver = person).order_by('-id')

    paginate = Paginator(notifications, 3)

    context = {
        'notifications': paginate.page(page),
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'all_notifications.html', context)


# Notifications
@login_required
def new_notifications(request):
    person = Person.objects.get(username = request.user.username)
    notifications = Notification.objects.filter(givver = person, done = False).order_by('-id')

    context = {
        'notifications': notifications,
    }

    for notification in notifications:
        notification.done = True
        notification.save()

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'new_notifications.html', context)


# Follow Person view
@login_required
def follow_person(request, username, url):
    person = Person.objects.get(username = username)

    user = Person.objects.get(username = request.user.username)

    if person in user.following.all():
        user.following.remove(person)
        user.len_following = int(user.len_following) - 1

        person.followers.remove(user)
        person.len_followers = int(person.len_followers) - 1
        

    else:
        user.following.add(person)
        user.len_following = int(user.len_following) + 1

        person.followers.add(user)
        person.len_followers = int(person.len_followers) + 1

        notif = Notification(givver = person, message = '<a href="/user/{0}/">{1}</a> از حالا شما را دنبال می‌کند'.format(user.username, user.name), notif_type = 'follow')
        notif.save()

    person.save()
    user.save()

    return HttpResponseRedirect(url.replace('%2F', '/'))


# Followed Persons view
@login_required
def friends(request, page):
    person = Person.objects.get(username = request.user.username)

    paginate = Paginator(person.following.all(), 3)
            
    context = {
        'persons': paginate.page(page),
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'followed_persons.html', context)


# Followed Persons Posts view
@login_required
def friends_posts(request, page):
    person = Person.objects.get(username = request.user.username)

    posts = []
    all_posts = Post.objects.all().order_by('-publish_time')
    for post in all_posts:
        if post.author in person.following.all():
            post.body = post.body.replace('<br/>', ' ')
            posts.append(post)

    paginate = Paginator(posts, 3)
            
    context = {
        'person': person,
        'posts': paginate.page(page),
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'friends_posts.html', context)


# Followers view
def followers(request, username, page):
    person = Person.objects.get(username = username)

    followers_available = False
    if len(person.followers.all()) > 0:
        followers_available = True

    paginate = Paginator(person.followers.all(), 3)
            
    context = {
        'persons': paginate.page(page),
        'person': person,
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
        'followers_available': followers_available,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'followers.html', context)


# Followers view
def followings(request, username, page):
    person = Person.objects.get(username = username)

    following_available = False
    if len(person.following.all()) > 0:
        following_available = True

    paginate = Paginator(person.following.all(), 3)
            
    context = {
        'persons': paginate.page(page),
        'person': person,
        'current_url': str('/user/friends/%3Fpage=1/').replace('/', '%2F'),
        'following_available': following_available,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'followings.html', context)