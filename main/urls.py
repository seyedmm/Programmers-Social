from django.urls import path
from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', views.index, name = 'index'),
    path('?page=<int:page>/', views.posts, name = 'posts'),
    path('wellcome/', views.wellcome, name = 'wellcome'),
    path('support/', views.support, name = 'support'),
    path('rocket/', views.rocket, name = 'rocket'),

    # Feeds
    path("feed/", LatestPostsFeed(), name="post_feed"),
]