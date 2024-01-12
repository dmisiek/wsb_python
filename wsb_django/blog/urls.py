from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_index, name='post.index'),
    path('<int:id>', views.post_show, name='post.show'),
    path('create', views.post_create, name='post.create'),
    path('login', views.auth_login, name='auth.login'),
    path('logout', views.auth_logout, name='auth.logout'),
]
