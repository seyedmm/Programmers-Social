from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.functions import mskf
import json
import re
import random

# Models
from main.models import Person,\
                        Post,\
                        PostComment,\
                        Notification,\
                        Ad

# Forms
from .forms import PostForm,\
                   CommentForm


# All Posts view
def all_posts(request, username, page):
    person = Person.objects.get(username = username) # Get the Person
    posts = Post.objects.filter(author = person).order_by('-publish_time') # Get the Posts

    try:
        user = Person.objects.get(username = request.user.username)
    
    except:
        user = None

    paginate = Paginator(posts, 3)

    context = {
        'posts': paginate.page(page),
        'person': person,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'all_posts.html', context)


# Post page view
def post_detail(request, username, post_id):
    person = Person.objects.get(username = username) # Get the Person
    post = get_object_or_404(Post, author = person, id = post_id) # Get the Post
    comments = PostComment.objects.filter(place = post).order_by('id') # Get the Comments
    len_comments = len(comments) # Get length of comments

    try:
        user = Person.objects.get(username = request.user.username)
    
    except:
        user = None

    post.views = int(post.views) + 1
    post.save()

    authenticated_user = None
    if request.user.is_authenticated:
        authenticated_user = Person.objects.get(username = request.user.username)
        authenticated_user.viewed_posts.add(post)
        authenticated_user.save()

    # For comment
    # If form method == POST
    if request.method == 'POST':
        print('post')
        form = CommentForm(request.POST) # Get form

        if form.is_valid():
            print('valid')
            mode = form.cleaned_data['mode'] # Read mode
            text = form.cleaned_data['text'] # Read body
            text = text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>') # Clean the body and recognize line breaks
            

            # If mode == comment
            if mode == 'comment':
                # Create a Comment model with form data
                comment = PostComment(place = post, author = user, text = text, replay = None)
                comment.save() # Save it

                post.comments = int(post.comments) + 1
                post.save()

                notif = Notification(givver = post.author, message = '<a href="/user/{0}/">{1}</a> نظری روی مطلب «<a href="/user/{2}/post/{3}/">{4}</a>» شما ارسال کرد'.format(user.username, user.name, post.author.username, post.id, post.title, comment.id), notif_type = 'comment')
                notif.save()

            elif mode == 'hello':
                return HttpResponse(json.dumps({'message': 'hello'}))

            else:
                comment = PostComment.objects.get(id = mode)
                comment.replay = text
                comment.save()

                notif = Notification(givver = comment.author, message = '<a href="/user/{0}/">{1}</a> پاسخی به <a href="/user/{2}/post/{3}/#comments">نظر</a> شما داد'.format(person.username, person.name, post.author.username, post.id), notif_type = 'replay')
                notif.save()

            context = {
                'post': post,
                'comments': comments,
                'len_comments': len_comments,
                'form': form,
                'current_url': str(request.path).replace('/', '%2F'),
            }

            mskf.add_notification_availability_to_context(request, context)
            mskf.add_authenticated_user_to_context(request, context)
            mskf.add_3_ads_to_context(context)

            return HttpResponseRedirect('/user/' + post.author.username + '/post/' + str(post.id))

    # If form method == GET
    else:
        form = CommentForm() # Give form to user

    
    post_body = mskf.get_repo_data(post.body)

    context = {
        'post': post,
        'post_body': post_body,
        'comments': comments,
        'len_comments': len_comments,
        'form': form,
        'person': user,
        'current_url': str(request.path).replace('/', '%2F'),
    }
    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)
    mskf.add_3_ads_to_context(context)

    return render(request, 'post_detail.html', context)


# Write post page view
@login_required
def new_post(request):
    person = Person.objects.get(username = request.user.username)

    # If form method == POST
    if request.method == 'POST':
        form = PostForm(request.POST) # Get form

        if form.is_valid():
            title = form.cleaned_data['title'] # Read title
            body = form.cleaned_data['body'] # Read body
            cover = form.cleaned_data['cover'] # Read cover
            short_description = form.cleaned_data['short_description'] # Read short description
            category = form.cleaned_data['category'] # Read category

            body = mskf.translate_to_html(body)

            # Create a Post model with form data
            post = Post(title = title,\
                        body = body,\
                        author = person,\
                        cover = cover,\
                        short_description = short_description,\
                        category = category)
            post.save() # Save it
            

            return HttpResponseRedirect('/user/' + post.author.username + '/post/' + str(post.id))

    # If form method == GET
    else:
        form = PostForm() # Give form to user

    context = {
        'form': form,
    }

    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'new_post.html', context)


# Edit post page view
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id = post_id) # Get the Post

    # If registered user is post author
    if post.author.username == request.user.username:
        # If form method == POST
        if request.method == 'POST':
            form = PostForm(request.POST) # Get form

            if form.is_valid():
                title = form.cleaned_data['title'] # Read title
                body = form.cleaned_data['body'] # Read body
                cover = form.cleaned_data['cover'] # Read cover
                short_description = form.cleaned_data['short_description'] # Read short description
                category = form.cleaned_data['category'] # Read category

                body = mskf.translate_to_html(body)

                # Give new data to post
                post.title = title 
                post.body = body
                post.cover = cover
                post.short_description = short_description
                post.category = category
                post.save() # Save it
                

                return HttpResponseRedirect('/user/' + post.author.username + '/post/' + str(post.id))

        # If form method == GET
        else:
            # Give form to user
            form = PostForm(initial = {
                                        'title': post.title,
                                        'body': mskf.translate_to_raw(post.body),
                                        'cover': post.cover,
                                        'short_description': post.short_description,
                                        'category': post.category,
                                    }) 

        context = {
            'form': form,
            'post': post,
        }

        mskf.add_notification_availability_to_context(request, context)
        mskf.add_authenticated_user_to_context(request, context)

        return render(request, 'edit_post.html', context)
    
    # If registered user not post author
    mskf.add_notification_availability_to_context(request, context)
    mskf.add_authenticated_user_to_context(request, context)

    return render(request, 'forbidden.html')


# Post delete view
@login_required
def delete_post(request, username, post_id):
    person = Person.objects.get(username = username)
    post = get_object_or_404(Post, author = person, id = post_id) # Get the Post

    # If registered user is post author
    if post.author.username == request.user.username:
        post.delete() # Delete it

        return HttpResponseRedirect('/' + 'user/' + username)

    # If registered user not post author
    else:
        context = {}

        mskf.add_notification_availability_to_context(request, context)
        mskf.add_authenticated_user_to_context(request, context)

        return render(request, 'forbidden.html', context)


# Post Comment delete view
@login_required
def delete_post_comment(request, username, post_id, comment_id):
    comment = get_object_or_404(PostComment, id = comment_id) # Get the Comment
    post = get_object_or_404(Post, id = post_id) # Get the Post

    # If registered user is comment author
    if comment.author.username == request.user.username:
        comment.delete() # Delete it

        post.comments = int(post.comments) - 1
        post.save()

        return HttpResponseRedirect('/user/' + username + '/post/' + str(post.id))

    # Or if registered user is comments post author
    elif post.author.username == request.user.username:
        comment.delete() # Delete it

        post.comments = int(post.comments) - 1
        post.save()

        return HttpResponseRedirect('/user/' + username + '/post/' + str(post.id))

    # If registered user not post author
    else:
        mskf.add_notification_availability_to_context(request, context)
        mskf.add_authenticated_user_to_context(request, context)

        return render(request, 'forbidden.html')


# Post Comment Replay delete view
@login_required
def delete_post_comment_replay(request, username, post_id, comment_id):
    comment = get_object_or_404(PostComment, id = comment_id) # Get the Comment
    post = get_object_or_404(Post, id = post_id) # Get the Post

    # if registered user is comments post author
    if post.author.username == request.user.username:
        comment.replay = None # Delete Comment Replay (set it None)
        comment.save() # Save it

        return HttpResponseRedirect('/user/' + username + '/post/' + str(post.id))

    # If registered user not post author
    else:
        mskf.add_notification_availability_to_context(request, context)
        mskf.add_authenticated_user_to_context(request, context)

        return render(request, 'forbidden.html')


# Like Post view
@login_required
def post_like(request, username, post_id):
    user = request.user
    person = Person.objects.get(username = user.username)
    person_likes = person.likes.all()
    post = Post.objects.get(id = post_id)

    if post in person_likes:
        post.likes = int(post.likes) - 1
        person.likes.remove(post)

    else:
        post.likes = int(post.likes) + 1
        person.likes.add(post)

        notif = Notification(givver = post.author, message = '<a href="/user/{0}/">{1}</a> مطلب «<a href="/user/{2}/post/{3}/">{4}</a>» شما را لایک کرد'.format(person.username, person.name, post.author.username, post.id, post.title), notif_type = 'like')
        notif.save()

    person.save()
    post.save()

    return HttpResponseRedirect('/user/' + username + '/post/' + str(post.id))
    