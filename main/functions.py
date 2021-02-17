# THE CODE IS CLEAN

import re
import os
from random import sample

import markdown
from bleach.linkifier import Linker
from six.moves.urllib.parse import urlparse
from PIL import Image, UnidentifiedImageError
from github import Github

# Models
from main.models import Person, Notification, Ad


# Delete all html tags
def no_html(text):
    html_tags = re.findall(r'<[^<>]*>', text)
    for tag in html_tags:
        clean_tag = tag.replace('<', '&lt;').replace('>', '&gt;')
        text = text.replace(tag, clean_tag)

    code_boxes = re.findall(r'```[^```]*```', text)
    for code_box in code_boxes:
        new_code_box = code_box.replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace(code_box, new_code_box)

    codes = re.findall(r'`[^`]*`', text)
    for code in codes:
        new_code = code.replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace(code, new_code)

    return text


# Get 3 ads
def ads_list():
    try:
        ads = Ad.objects.filter(type='پایین مطلب')

        ads_list = []
        for ad in ads:
            if ad.available_views == '0':
                ad.delete()

            else:
                ads_list.append(ad)
                ad.available_views = int(ad.available_views) - 1
                ad.save()

        if len(ads_list) < 1:
            ads_list.append(None)
            ads_list.append(None)
            ads_list.append(None)

        elif len(ads_list) < 2:
            ads_list.append(None)
            ads_list.append(None)

        elif len(ads_list) < 3:
            ads_list.append(None)

        else:
            ad1, ad2, ad3 = sample(ads_list, 3)
            ads_list = []

            ads_list.append(ad1)
            ads_list.append(ad2)
            ads_list.append(ad3)

    except:
        ads_list = None

    return ads_list


# Get Github Repository Data
def get_repo_data(text):
    text = text.replace('{% گیت هاب ', '▸').replace(' %}', '◂').replace(
        '{٪ گیت هاب ', '▸').replace(' ٪}', '◂')
    repos = re.findall(r'▸[^▸◂]*◂', text)

    for repo_name in repos:
        GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
        g = Github(GITHUB_TOKEN)

        try:
            repo = g.get_repo(repo_name.replace('▸', '').replace('◂', ''))

            try:
                repo_license = repo.get_license().license.name

            except:
                repo_license = 'None'

            repo_html = f'''<a href="https://github.com/{repo.full_name}/" target="_blank" rel="noopener nofollow">
                <div dir="ltr" class="jumbotron" style="text-align: left; padding: 1rem 1rem; background: var(--light-hover);">
                    <h5 style="font-family: Vazir; font-weight: 400;">
                        <img class="avatar" type="button" src="{repo.owner.avatar_url}" width="48px" height="48px">
                        {repo.full_name}
                    </h5>
                    <p>{repo.description}</p>
                    <p>
                        <span class="badge" style=" font-size: 1em; font-weight: lighter;">
                            <i class="fas fa-code"></i> {repo.language}
                        </span>
                        <span class="badge" style=" font-size: 1em; font-weight: lighter;">
                            <i class="fas fa-balance-scale"></i> {repo_license}
                        </span>
                        <span class="badge" style=" font-size: 1em; font-weight: lighter;">
                            <i class="far fa-star"></i> {repo.stargazers_count}
                        </span>
                    </p>
                </div>
            </a>
            '''.replace('\n', '')

        except:
            repo_html = '<a href="https://github.com/{0}/" target="_blank" rel="noopener nofollow">https://github.com/{0}/</a>'.format(repo_name.replace('▸', '').replace('◂', ''))

        text = text.replace(repo_name, repo_html)

    return text.replace('▸', '{ گیت هاب ').replace('◂', ' }')


# Get the authenticated user, if user is authenticated
def get_authenticated_user(request):
    if request.user.is_authenticated:
        return Person.objects.get(username=request.user.username)

    return None


# Get the authenticated user unread notifications
def get_new_notifications(authenticated_user):
    if authenticated_user is not None:
        return len(
            Notification.objects.filter(
                givver=authenticated_user,
                done=False
            )
        )

    return 0


# Compress the image
def compress_image(path):
    try:
        file_path = path
        img = Image.open(file_path)
        img.save(
            file_path,
            quality=50,
            optimize=True)

    except UnidentifiedImageError:
        pass


# translate markdown to html
def translate_to_html(text):
    def set_target(attrs, new=False):
        p = urlparse(attrs[(None, 'href')])
        if p.netloc not in ['localhost:8000']:
            attrs[(None, 'rel')] = 'noopener nofollow'
            attrs[(None, 'target')] = '_blank'

        return attrs

    linker = Linker(callbacks=[set_target])

    return linker.linkify(
        markdown.markdown(
            get_repo_data(
                no_html(text)
            ),
            extensions=[
                'markdown.extensions.codehilite',
                'markdown.extensions.fenced_code',
                'markdown.extensions.sane_lists',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
            ],
        )
    )
