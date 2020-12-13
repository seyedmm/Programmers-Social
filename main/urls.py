from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('?page=<int:page>/', views.posts, name = 'posts'),
    path('wellcome/', views.wellcome, name = 'wellcome'),
    # path('support/', views.posts, name = 'support'),
]