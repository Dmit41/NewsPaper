from email.headerregistry import Group

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostListSearch(PostList):
    template_name = 'post_search.html'
    context_object_name = 'all_news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = "NW"
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_articles',)
    model = Post
    form_class = NewsForm
    template_name = 'article_create.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_news',)
    form_class = NewsForm
    model = Post
    template_name = 'post_update.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_news',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def update_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user.set.add(user)
    return redirect('/news')


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def add_subs(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались'
    return render(request, 'add_subs.html', {'category': category, 'message': message})


@login_required
def del_subs(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписались'
    return render(request, 'del_subs.html', {'category': category, 'message': message})
