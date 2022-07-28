from django.forms import ModelForm
from .models import Post, User
from django.core.exceptions import ValidationError
from django import forms


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control pure-input-1-2'}),
            'title': forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
            'text': forms.Textarea(attrs={'class': 'form-control pure-input-1-2'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Статья не может быть менее 20 символов."
            })

        return cleaned_data


class AuthorForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
