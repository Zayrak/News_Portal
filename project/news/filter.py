import django.forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category, Author

class PostFilter(FilterSet):
    dateCreation = DateFilter(lookup_expr = 'gt',
        widget=django.forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    categoryThrough = ModelChoiceFilter(
        field_name = 'postCategory',
        queryset = Category.objects.all(),
        label = 'Категория',
        empty_label = 'Любой'
    )
    authorThrough = ModelChoiceFilter(
        field_name = 'author',
        queryset = Author.objects.all(),
        label = 'Автор',
        empty_label = 'Любой'
    )


    class Meta:
       model = Post
       fields = {
           'title': ['icontains'],

       }
