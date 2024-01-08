from django.shortcuts import render, HttpResponse

from .models import Post, Comment


# Create your views here.
def post_index(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'post_index.html', context)

def post_show(request, id):
    post = Post.objects.get(id=id)
    context = {
        'post': post,
        'comments': Comment.objects.filter(post=post)
    }

    return render(request, 'post_show.html', context)