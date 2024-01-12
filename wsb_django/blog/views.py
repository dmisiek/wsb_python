from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Post, Comment
from .forms import LoginForm, CommentCreateForm, PostForm


# Create your views here.
def post_index(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at')
    }

    return render(request, 'post_index.html', context)

def post_show(request, pk):
    post = Post.objects.get(id=pk)
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
                return redirect('auth.login')

            context['form'] = CommentCreateForm()

    return render(request, 'post_show.html', context)

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('auth.login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                title=form.cleaned_data.get('title'),
                content=form.cleaned_data.get('content'),
                author=request.user
            )
            return redirect('post.show', pk=post.id)
    else:
        form = PostForm()

    return render(request, 'post_create.html', {'form': form})

def post_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('auth.login')

    post = Post.objects.get(id=pk)

    if post.author != request.user:
        return redirect('post.show', pk=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.filter(id=pk).update(
                title=form.cleaned_data.get('title'),
                content=form.cleaned_data.get('content'),
                author=post.author,
            )
            return redirect('post.show', pk=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_update.html', {'form': form, 'post': post})

def post_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('auth.login')

    post = Post.objects.get(id=pk)

    if post.author != request.user:
        return redirect('post.show', pk=post.id)

    if request.method == 'POST':
        post.delete()
        return redirect('post.index')

    return render(request, 'post_delete.html', {'post': post})

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
