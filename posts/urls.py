from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('<str:username>/post/all/?page=<int:page>/', views.all_posts, name = 'all_posts'),
    path('post/new/', views.new_post, name = 'new_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name = 'edit_post'),
    path('<str:username>/post/<int:post_id>/delete/', views.delete_post, name = 'delete_post'),
    path('<str:username>/post/<int:post_id>/', views.post_detail, name = 'post_detail'),
    path('<str:username>/post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_post_comment, name = 'delete_post_comment'),
    path('<str:username>/post/<int:post_id>/like/', views.post_like, name = 'post_like'),
]