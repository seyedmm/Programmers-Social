from django.urls import path, include
from . import views


app_name = 'person'
urlpatterns = [
    path('all/?page=<int:page>/', views.all_persons, name = 'all_persons'),
    path('notifications/all/?page=<int:page>/', views.all_notifications, name = 'all_notifications'),
    path('notifications/new/', views.new_notifications, name = 'new_notifications'),
    path('settings/edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('settings/edit_rezome/', views.edit_rezome, name = 'edit_rezome'),
    path('<str:username>/follow/url=<str:url>/', views.follow_person, name = 'follow_person'),
    path('friends/?page=<int:page>/', views.friends, name = 'friends'),
    path('friends/posts/?page=<int:page>/', views.friends_posts, name = 'friends_posts'),
    path('', include('posts.urls')),
    path('<str:username>/', views.profile_detail, name = 'profile_detail'),
    path('<str:username>/rezome/', views.rezome_detail, name = 'rezome_detail'),
    path('<str:username>/followers/?page=<int:page>/', views.followers, name = 'followers'),
    path('<str:username>/followings/?page=<int:page>/', views.followings, name = 'followings'),
]