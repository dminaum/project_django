from .models import Product


class ProductService:

    @staticmethod
    def products_in_category(category_id):
        products = Product.objects.filter(category_id=category_id)
        return products
