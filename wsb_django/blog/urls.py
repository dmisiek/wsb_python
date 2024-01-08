from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_index, name='post.index'),
    path('<int:id>', views.post_show, name='post.show'),
]
