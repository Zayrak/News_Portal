from django.urls import path
from .views import PostsList, PostsDetail, NewsSearch, PostsUpdate, PostsDelete, NewsCreate, ProfileUpdateView

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostsDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', PostsUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostsDelete.as_view(), name='post_delete'),
    path('<str:username>/profile_update/', ProfileUpdateView.as_view(), name='profile_update'),

]
