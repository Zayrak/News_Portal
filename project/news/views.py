from django.views.generic import (
                                    ListView, DetailView,
                                    CreateView, UpdateView, DeleteView,
                                  )
from .models import (
                        Post,
                        Category,
                        CatSub,
                     )

from .filters import PostFilter
from .forms import (
                    PostForm,
                    AuthorForm,
                    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 9
    form_class = PostForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=super().get_queryset())
        return context


class PostView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()
    paginate_by = 6
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=super().get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_create.html'
    form_class = PostForm #

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        validated = super().form_valid(form)
        return validated


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'new_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        post.isUpdated = True
        return post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    success_url = '/news/'
    template_name = 'new_delete.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_create.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        validated = super().form_valid(form)

        return validated


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user


class PostCategory(ListView):
    model = Post
    ordering = ['-date']
    template_name = 'subcat/filtered.html'
    context_object_name = 'news'
    paginate_by = 6


    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(category=Category.objects.get(id=self.id))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['name'] = Category.objects.get(id=self.id)
        return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if not cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.add(user)
        html = render_to_string(
            'subcat/subscribed.html',
            {'categories': cat, 'user': user},

        )
        msg = EmailMultiAlternatives(
            subject=f'На {cat} категорию подписаны',
            from_email='*******@yandex.ru',
            to=[user.email, ],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('profile')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.remove(user)
    return redirect('profile')


class ProfileView(ListView):
    model = CatSub
    template_name = 'profile.html'
    context_object_name = 'categories'

