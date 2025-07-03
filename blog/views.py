from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView
from .models import Post


class CreatePostView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('main-feed')
    context_object_name = 'post'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('main-feed')
    context_object_name = 'post'
