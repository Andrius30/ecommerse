from django import forms
from .models import User
from django.core.exceptions import ValidationError
import re


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already taken')
        if len(username) < 6:
            raise ValidationError('Username must be at least 6 characters long')

        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise ValidationError('Username can only contain letters, numbers, and underscores')

        if not re.search("[a-zA-Z]", username):
            raise ValidationError('Username must contain at least one letter')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords must match')

        if len(password1) < 12:
            raise ValidationError('Password must be at least 12 characters')

        if not re.search("^[a-zA-Z0-9_]+$", password1):
            raise ValidationError('Password can only contain letters, numbers, and underscores')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

    def clean_username(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('username')
        if not re.match("^[a-zA-Z0-9_]+$", user):
            raise ValidationError('Username can only contain letters, numbers, and underscores')

        return user

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if not re.match("^[a-zA-Z0-9_]+$", password):
            raise ValidationError('Password can only contain letters, numbers, and underscores')

        return password