from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-dateCreation'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'



