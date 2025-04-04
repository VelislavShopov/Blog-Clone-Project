from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from main_app.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email','password1','password2')