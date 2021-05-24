from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create_user', views.create_user),
    path('user/dashboard', views.dashboard),
    path('blog/user/dashboard', views.dashboard),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('blog/create_post', views.CreatePost),
    path('blog/blog_form', views.blog_form),
    path('blog/<int:post_id>', views.show_post),
    path('blog/<int:post_id>/delete', views.delete),
    path('user/<int:user_id>', views.user_page),
]