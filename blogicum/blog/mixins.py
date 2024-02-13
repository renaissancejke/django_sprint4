from django.shortcuts import redirect
from django.urls import reverse

from blog.forms import CommentForm
from blog.models import Comment


class DispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().author != request.user):
            return redirect('blog:post_detail', pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})
