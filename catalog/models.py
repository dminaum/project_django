from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=False, verbose_name='Статус публикации')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        related_name='products'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_delete_product", "Может удалять продукт"),
        ]
