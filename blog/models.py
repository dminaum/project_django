from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Изображение')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Публикации')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-created_at']
