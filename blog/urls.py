from django.urls import path
from .views import CreatePostView, PostDetailView, PostListView, UpdatePostView, DeletePostView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('feed/', PostListView.as_view(), name='main-feed'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post-delete')
]
