from django.urls import path
from .views import (NewsList, PostView,
                    PostSearch, PostCreateView, PostUpdateView, PostDeleteView, ArticleCreateView,
                    PostCategory, subscribe_to_category, unsubscribe_from_category, ProfileView
                    )


urlpatterns = [

    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', PostView.as_view(), name='new'),
    path('search/', PostSearch.as_view(), name='search'),
    path('search/<int:pk>', PostView.as_view(), name='new_search'),
    path('new/create/', PostCreateView.as_view(), name='new_create'),
    path('new/<int:pk>/edit', PostUpdateView.as_view(), name='new_update'),
    path('new/<int:pk>/delete', PostDeleteView.as_view(), name='new_delete'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', PostDeleteView.as_view(), name='article_delete'),
    path('category/<int:pk>', PostCategory.as_view(), name='post_category'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscr_category'),
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscr_category'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
