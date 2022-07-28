from django_filters import (FilterSet, CharFilter, ModelChoiceFilter,
                            DateFilter,
                            )
from .models import Post, Author, Category
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(
        label='Дата',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control pure-input-1-2'}),
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Название статьи',
        widget=forms.TextInput(attrs={'class': 'form-control pure-input-1-2', 'placeholder': 'Post Title'}),
    )
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
        # D6
        widget=forms.Select(attrs={'class': 'form-control pure-input-1-2'}),
    )

    class Meta:
        model = Post
        fields = ['date', 'title', 'author', 'category']
