from django import forms

from .models import Post


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Nazwa użytkownika")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł",
        widget=forms.TextInput(
            attrs={'placeholder': 'Podaj tytuł nowego postu'}
        )
    )
    content = forms.CharField(
        label="Treść",
        widget=forms.Textarea(
            attrs={'placeholder': 'Wpisz treść nowego postu...'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentCreateForm(forms.Form):
    content = forms.CharField(
        label="Treść komentarza",
        widget=forms.Textarea(
            attrs={'placeholder': 'Wpisz treść komentarza...'}
        )
    )
