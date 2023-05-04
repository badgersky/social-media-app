from django import forms

from posts import models


class CreatePostForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'title',
            'placeholder': 'Post Title',
        })
    )

    content = forms.TextInput(attrs={
        'name': 'title',
        'placeholder': 'Post Content',
    })

    class Meta:
        model = models.Tweet
        fields = ('title', 'content')
