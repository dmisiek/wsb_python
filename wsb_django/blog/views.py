from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Post, Comment
from .forms import LoginForm, CommentCreateForm


# Create your views here.
def post_index(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'post_index.html', context)

def post_show(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    context = {
        'post': post,
        'comments': comments,
        'form': None,
    }

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                content=form.cleaned_data.get('content'),
                post=post,
                author=request.user
            )
        else:
            if not request.user.is_authenticated:
                # TODO: Add redirect to prevoius page
                return redirect('auth.login')

            context['form'] = CommentCreateForm()

    return render(request, 'post_show.html', context)

def auth_login(request):
    if request.user.is_authenticated:
        return redirect('post.index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('post.index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def auth_logout(request):
    if not request.user.is_authenticated:
        return redirect('login.html')

    logout(request)
    return redirect('post.index')
