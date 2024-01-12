from django import forms

from .models import Post


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'bg-stone-700 text-sm', 'placeholder': 'Enter your comment...'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'bg-stone-700 text-sm', 'placeholder': 'Enter your comment...'}
        )
    )
