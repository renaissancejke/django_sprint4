from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import DeletionMixin

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.mixins import CommentMixin, DispatchMixin
from blog.models import Category, Comment, Post, User

MAX_POSTS = 10


class ProfileListView(ListView):
    model = Post
    paginate_by = MAX_POSTS
    template_name = 'blog/profile.html'

    def get_queryset(self):
        return (
            self.model.objects.select_related('author', 'category', 'location')
            .filter(author__username=self.kwargs['username'])
            .annotate(comment_count=Count("comment"))
            .order_by("-pub_date"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])


class IndexListView(ListView):
    model = Post
    paginate_by = MAX_POSTS
    template_name = 'blog/index.html'

    def get_queryset(self):
        return (
            self.model.objects.select_related('location', 'author', 'category')
            .filter(is_published=True,
                    category__is_published=True,
                    pub_date__lte=timezone.now())
            .annotate(comment_count=Count("comment"))
            .order_by("-pub_date"))


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=pk
    )
    if post.author != request.user:
        post = get_object_or_404(
            Post.objects.select_related('category', 'location', 'author')
            .filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True
            ),
            pk=pk
        )
    post_comments = Comment.objects.filter(post=post).select_related('author')
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': post_comments,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug, is_published=True
    )
    post_list = Post.objects.select_related('author').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
        category=category
    ).order_by('-pub_date').annotate(comment_count=Count('comment'))
    paginator = Paginator(post_list, MAX_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, DispatchMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def get_success_url(self):
        post = self.object
        return reverse('blog:post_detail', kwargs={'pk': post.pk})


class PostDeleteView(DeletionMixin, PostUpdateView):
    success_url = reverse_lazy('blog:index')


@login_required
def add_comment(request, post_id, comment_id=None):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_id)


class CommentUpdateView(LoginRequiredMixin, DispatchMixin,
                        CommentMixin, UpdateView):
    pass


class CommentDeleteView(LoginRequiredMixin, DispatchMixin,
                        CommentMixin, DeleteView):
    pass
