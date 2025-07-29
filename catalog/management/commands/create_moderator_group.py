from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        content_type = ContentType.objects.get_for_model(Product)

        try:
            can_unpublish = Permission.objects.get(
                codename='can_unpublish_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Право can_unpublish_product не найдено. Проверь миграции.'))
            return

        try:
            can_delete = Permission.objects.get(
                codename='can_delete_product',
                content_type=content_type
            )
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Право can_delete_product не найдено. Проверь миграции.'))
            return

        # Назначаем права
        group.permissions.set([can_unpublish, can_delete])
        group.save()

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана и настроена.'))
