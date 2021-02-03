from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from main.models import Post
from django.urls import reverse
from django.conf import settings



class CustomFeed(Atom1Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement("image", item["image"])


class LatestPostsFeed(Feed):
    feed_type = CustomFeed
    title = "شبکه اجتماعی برنامه نویسان"
    link = ""
    description = "جدیدترین مطالب"

    def items(self):
        return Post.objects.all().order_by('-publish_time')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_author_name(self, item):
        return item.author.name

    def item_extra_kwargs(self, item):
        return {'image': item.cover}


    def item_link(self, item):
        return reverse("person:post:post_detail", args=[item.author.username, item.id])