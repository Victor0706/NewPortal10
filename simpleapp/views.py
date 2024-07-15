from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import NewForm, ArticleForm
from simpleapp.models import Post, Subscription, Category

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import logging

logger = logging.getLogger(__name__)


class PostList(ListView):
    model = Post
    ordering = '-added_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
        return Post.objects.filter.order_by('-added_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='NW')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='AR')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'simpleapp.add_post'
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'simpleapp.add_post'
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'simpleapp.change_post'
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='NW')


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'simpleapp.change_post'
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='AR')


class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'simpleapp.delete_post'
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='NW')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'simpleapp.delete_post'
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category_type='AR')


class NewSearch(ListView):
    model = Post
    ordering = '-added_at'
    template_name = 'new_search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
        return Post.objects.filter.order_by('-added_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )



