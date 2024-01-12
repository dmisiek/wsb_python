from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_index, name='post.index'),
    path('create', views.post_create, name='post.create'),
    path('<int:pk>', views.post_show, name='post.show'),
    path('<int:pk>/update', views.post_update, name='post.update'),
    path('<int:pk>/delete', views.post_delete, name='post.delete'),
    path('login', views.auth_login, name='auth.login'),
    path('logout', views.auth_logout, name='auth.logout'),
]
