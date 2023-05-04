from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from . import models


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'placeholder': 'Password',
        })
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'name': 'confirm_password',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(f'Passwords don`t match')

        validate_password(confirm_password)

        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if models.CustomUser.objects.filter(username=username).exists():
            raise ValidationError(f'Try using different username')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if models.CustomUser.objects.filter(email=email).exists():
            raise ValidationError(f'Try using different email')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.clean_confirm_password())
        user.is_active = True

        if commit:
            user.save()

        return user
