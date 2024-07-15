from django.urls import path
from .views import (
    PostList, NewDetail, NewCreate, NewUpdate, NewDelete, NewSearch, ArticleDetail, ArticleCreate,
    ArticleUpdate, ArticleDelete, subscriptions
)
from django.views.decorators.cache import cache_page


urlpatterns = [
path('', cache_page(60 * 1)(PostList.as_view()), name='post_list'),
path('news/<int:id>', cache_page(60 * 5)(NewDetail.as_view()), name='new_detail'),
path('news/create/', NewCreate.as_view(), name='new_create'),
path('news/<int:id>/update/', NewUpdate.as_view(), name='new_update'),
path('news/<int:id>/delete/', NewDelete.as_view(), name='new_delete'),
path('search/', NewSearch.as_view(), name='new_search'),
path('subscriptions/', subscriptions, name='subscriptions'),
path('articles/<int:id>', cache_page(60 * 5)(ArticleDetail.as_view()), name='article_detail'),
path('articles/create/', ArticleCreate.as_view(), name='article_create'),
path('articles/<int:id>/update/', ArticleUpdate.as_view(), name='article_update'),
path('articles/<int:id>/delete/', ArticleDelete.as_view(), name='article_delete'),
]



