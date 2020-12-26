# THE CODE IS CLEAN

import re
import os
from random import sample

# Models
from main.models import Person,\
                        Notification,\
                        Ad
                        

# MSKF
class mskf():
    def add_notification_availability_to_context(request, context):
        if request.user.is_authenticated:
            person = Person.objects.get(username=request.user.username)

            notification = Notification.objects.filter(
                givver=person,
                done=False)

            new_notif = False
            if len(notification) > 0:
                new_notif = True

            context['new_notif'] = new_notif
            context['notif_len'] = len(notification)


    def add_authenticated_user_to_context(request, context):
        if request.user.is_authenticated:
            authenticated_user = Person.objects.get(username=request.user.username)
            context['authenticated_user'] = authenticated_user


    def translate_to_html(text):
        text = text.replace('<', '&lt;').replace('>', '&gt;').replace(
            '\n', '<br/>')  # Clean the text and recognize line breaks

        def except_(exceptions_dic, text):
            # Exceptions
            text = text.replace('__', '◼')
            exceptions = re.findall(r'◼[^◼]*◼', text)
            for e in exceptions:
                excepted = e
                for key, value in exceptions_dic.items():
                    excepted = excepted.replace(key, value)
                text = text.replace(e, excepted)

            return text

        # Recognize bolds
        text = text.replace('**', '◆')
        bold_texts = re.findall(r'◆[^◆]*◆', text)
        for bold_text in bold_texts:
            html_text = '<strong>' + \
                bold_text.replace('◆', '') + '</strong>'
            text = text.replace(bold_text, html_text)

        text = text.replace('◆', '**')

        # Recognize italics
        text = text.replace('*', '◆')
        italic_texts = re.findall(r'◆[^◆]*◆', text)
        for italic_text in italic_texts:
            html_text = '<i>' + italic_text.replace('◆', '') + '</i>'
            text = text.replace(italic_text, html_text)

        text = text.replace('◆', '*')

        # Recognize titrs
        text = text.replace('###', '◆')
        text = text.replace('<br/>', '\n')
        titr_texts = re.findall(r'\n◆.*', text)
        for titr_text in titr_texts:
            html_text = '</p><h3>' \
                      + titr_text[1:].replace('◆', '') \
                      + '</h3><p>'
            text = text.replace(titr_text, html_text)

        text = text.replace('\n', '<br/>')
        text = re.sub(
            r'\</h3><p>[^<]*\<br/>', lambda x: x.group(0).replace('<br/>', ''), text)

        text = text.replace('◆', '###')

        # Regingize images
        text = text.replace(')(', '◆').replace('!(', '▸').replace(')', '◂')
        text = except_({'◆': ')(', '▸': '(', '◂': ')'}, text)
        image_texts = re.findall(r'▸[^▸◆◂]*◆[^▸◆◂]*◂', text)
        for image_text in image_texts:
            image_alt = re.findall(r'▸[^▸◆◂]*◆', image_text)[0]
            image_url = re.findall(r'◆[^▸◆◂]*◂', image_text)[0]
            html_text = '<div class="img"><img src=\"' + image_url.replace('◆', '').replace(
                '◂', '') + '\" alt=\"' + image_alt.replace('▸', '').replace('◆', '') + '\"></div>'
            text = text.replace(image_text, html_text)

        text = text.replace('▸', '!(').replace('◂', ')')

        # Recognize links
        text = text.replace(')(', '◆').replace('(', '▸').replace(')', '◂')
        text = except_({'◆': ')(', '▸': '(', '◂': ')'}, text)
        link_texts = re.findall(r'▸[^▸◆◂]*◆[^▸◆◂]*◂', text)
        for link_text in link_texts:
            link_name = re.findall(r'▸[^▸◆◂]*◆', link_text)[0]
            link = re.findall(r'◆[^▸◆◂]*◂', link_text)[0]
            html_text = '<a href=\"' \
                      + link.replace('◆', '').replace('◂', '') \
                      + '\" target=\"_blank\" rel=\"noopener nofollow\">' \
                      + link_name.replace('▸', '').replace('◆', '') \
                      + '</a>'
            text = text.replace(link_text, html_text)

        text = text.replace('▸', '(').replace('◆', ')(').replace('◂', ')')

        # Recognize code boxes
        text = text.replace('```', '◆')
        code_texts = re.findall(r'◆[^◆]*◆', text)
        for code_text in code_texts:
            html_text = '</p><pre id="code">' + \
                code_text.replace('◆', '').replace(
                    '<br/>', '') + '</pre><p>'
            text = text.replace(code_text, html_text)

        text = re.sub(
            r'\</pre><p>[^<]*\<br/>', lambda x: x.group(0).replace('<br/>', ''), text)

        text = text.replace('◆', '```')

        # Recognize codes
        text = text.replace('`', '◆')
        code_texts = re.findall(r'◆[^◆]*◆', text)
        for code_text in code_texts:
            html_text = '<code>' + code_text.replace('◆', '') + '</code>'
            text = text.replace(code_text, html_text)

        text = text.replace('◆', '`')

        # Recognize lists
        text = text.replace('-', '◆')
        text = text.replace('<br/>', '\n')
        link_texts = re.findall(r'\n◆.*', text)
        for link_text in link_texts:
            html_text = '<li>' + link_text[1:].replace('◆', '').replace('\n', '') + '</li>'
            text = text.replace(link_text, html_text)

        text = text.replace('\n', '▸').replace('</li>▸', '</li>')

        lists = re.findall(r'<li>[^▸]*</li>', text)
        print(lists)
        for listt in lists:
            complete_list = '<ul>' + listt + '</ul>'
            text = text.replace(listt, complete_list)

        text = text.replace('▸', '<br/>')
        text = text.replace('◆', '-')

        # Recognize gists
        text = text.replace('{ گیست ', '▸').replace(' }', '◂')
        gists = re.findall(r'▸[^▸◂]*◂', text)
        for gist in gists:
            gist_code = '<script src="https://gist.github.com/' \
                      + gist.replace('▸', '').replace('◂', '') \
                      + '.js"></script>'
            text = text.replace(gist, gist_code)

        text = text.replace('▸', '{ گیست ').replace('◂', ' }')

        return text.replace('◼', '')


    def translate_to_raw(text):
        # HTML bold to RAW
        text = text.replace('<strong>', '**').replace('</strong>', '**')

        # HTML italic to RAW
        text = text.replace('<i>', '*').replace('</i>', '*')

        # HTML titr to RAW
        text = text.replace('</p><h3>', '###').replace('</h3><p>', '')

        # HTML code to RAW
        text = text.replace('<code>', '`').replace('</code>', '`')

        # HTML code box to RAW
        text = text.replace('</p><pre id="code">', '```').replace('</pre><p>', '```')

        # HTML list to RAW
        text = text.replace('<ul>', '').replace('</ul>', '').replace('</li>', '').replace('<li>', '-')

        # HTML link to RAW
        text = text.replace('\" target=\"_blank\" rel=\"noopener nofollow\">', '◆').replace('<a href=\"', '▸').replace('</a>', '◂')
        html_links = re.findall(r'▸[^▸◆◂]*◆[^▸◆◂]*◂', text)
        links = re.findall(r'▸[^▸◆◂]*◆', text)
        link_alts = re.findall(r'◆[^▸◆◂]*', text)

        for num, item in enumerate(html_links):
            if '(' in links[num] or ')' in links[num]:
                raw_link = '(' \
                         + link_alts[num].replace('◆', '').replace('◂', '') \
                         + ')(__' \
                         + links[num].replace('▸', '').replace('◆', '') \
                         + '__)'

            else:
                raw_link = '(' \
                         + link_alts[num].replace('◆', '').replace('◂', '') \
                         + ')(' \
                         + links[num].replace('▸', '').replace('◆', '') \
                         + ')'

            text = text.replace(item, raw_link)

        text = text.replace('◆', '\" target=\"_blank\" rel=\"noopener nofollow\">').replace('▸', '<a href=\"').replace('◂', '</a>')

        # HTML image to RAW
        text = text.replace('\" alt=\"', '◆').replace('<div class="img"><img src=\"', '▸').replace('\"></div>', '◂')
        html_images = re.findall(r'▸[^▸◆◂]*◆[^▸◆◂]*◂', text)
        images = re.findall(r'▸[^▸◆◂]*◆', text)
        image_alts = re.findall(r'◆[^▸◆◂]*◂', text)

        for num, item in enumerate(html_images):
            if '(' in images[num] or ')' in images[num]:
                raw_image = '!(' \
                          + image_alts[num].replace('◆', '').replace('◂', '') \
                          + ')(__' \
                          + images[num].replace('▸', '').replace('◆', '') \
                          + '__)'

            else:
                raw_image = '!(' \
                          + image_alts[num].replace('◆', '').replace('◂', '') \
                          + ')(' \
                          + images[num].replace('▸', '').replace('◆', '') \
                          + ')'

            text = text.replace(item, raw_image)

        text = text.replace('◆', '\" alt=\"').replace('▸', '<div class="img"><img src=\"').replace('◂', '\"></div>')

        # HTML gist to RAW
        text = text.replace('<script src="https://gist.github.com/', '{ گیست ').replace('.js"></script>', ' }')

        # Clean the text and recognize line breaks
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('<br/>', '\n') 

        return text


    def compress(path):
        from PIL import Image
        try:
            file_path = path
            img = Image.open(file_path)
            img.save(
                file_path,
                quality=50,
                optimize=True)

        except:
            pass

    def add_3_ads_to_context(context):
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

        context['ads_list'] = ads_list


    # Get Github Repository Data
    def get_repo_data(text):
        text = text.replace('{ گیت هاب ', '▸').replace(' }', '◂')
        repos = re.findall(r'▸[^▸◂]*◂', text)
        for repo_name in repos:
            from github import Github
            GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
            g = Github(GITHUB_TOKEN)

            try:
                repo = g.get_repo(repo_name.replace('▸', '').replace('◂', ''))

                repo_full_name = repo.full_name
                repo_description = repo.description
                repo_lang = repo.language
                repo_stars = repo.stargazers_count
                repo_owner_avatar = repo.owner.avatar_url

                try:
                    repo_license = repo.get_license().license.name

                except:
                    repo_license = 'None'

                repo_html = '''
                    <div dir="ltr" class="jumbotron"
                        style="text-align: left; padding: 1rem 1rem; background: var(--light); border: 1px solid var(--border-color);">

                        <h5 style="font-family: Vazir; font-weight: 400;">
                        <img class="avatar border-gray" type="button" src="{repo_owner_avatar}"
                            width="48px" height="48px" style="border-style: solid; border-width: 1px;">
                        <a href="https://github.com/{repo_full_name}/" target="_blank" rel="noopener nofollow"> {repo_full_name}</a>
                        </h5>
                        <p>{repo_description}</p>
                            <span class="badge" style=" font-size: 1em; font-weight: lighter;"><i class="fas fa-code"></i> {repo_lang}</span>

                            <span class="badge" style=" font-size: 1em; font-weight: lighter;"><i class="fas fa-balance-scale"></i> {repo_license}</span>

                            <span class="badge" style=" font-size: 1em; font-weight: lighter;"><i class="far fa-star"></i> {repo_stars}</span>
                    </div>
                '''.format(repo_full_name=repo_full_name,
                           repo_description=repo_description,
                           repo_license=repo_license,
                           repo_lang=repo_lang,
                           repo_stars=repo_stars,
                           repo_owner_avatar=repo_owner_avatar
                           )

            except:
                repo_html = '<a href="{repo_link}" target="_blank" rel="noopener nofollow">{repo_link}</a>'.format(repo_link='https://github.com/' + repo_name.replace('▸', '').replace('◂', ''))

            text = text.replace(repo_name, repo_html)

        return text.replace('▸', '{ گیت هاب ').replace('◂', ' }')
