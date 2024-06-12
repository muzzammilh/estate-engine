from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import User


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': forms.CharField}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")
        field_classes = {'username': forms.CharField}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'role', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', strip=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', strip=False, widget=forms.PasswordInput)
