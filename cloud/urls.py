# THE CODE IS CLEAN

from django.urls import path, include
from . import views


app_name = 'cloud'
urlpatterns = [
    path('', views.cloud_index, name='cloud_index'),
    path('upload/', views.upload_file, name='upload_file'),
    # path('<str:file_name>/delete/', views.delete_file, name = 'delete_file'),
]
