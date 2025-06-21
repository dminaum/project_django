from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаляет старые и добавляет тестовые продукты'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.WARNING('Все старые продукты и категории удалены.'))

        category = Category.objects.create(
            name='Тестовая категория',
            description='Описание тестовой категории'
        )

        products = [
            {'name': 'Тестовый мяч', 'price': 10.99},
            {'name': 'Тестовая футболка', 'price': 19.99},
            {'name': 'Тестовый ноутбук', 'price': 999.99},
        ]

        for data in products:
            product = Product.objects.create(
                name=data['name'],
                price=data['price'],
                category=category
            )
            self.stdout.write(self.style.SUCCESS(f'Добавлен продукт: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Готово! Все тестовые продукты добавлены.'))
