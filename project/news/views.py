from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from .forms import PostForm, UserForm
from .models import Post
from .filter import PostFilter
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-dateCreation'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = '-dateCreation'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class PostsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    form_class = UserForm
    success_url = '/news/'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self, **kwargs):
        return self.request.user


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'post'



class ChangePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'post'


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    form = PostForm
    return render(request, 'news_edit.html', {'form': form})
