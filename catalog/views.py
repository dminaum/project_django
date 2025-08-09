from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Category
from django.urls import reverse_lazy, reverse
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .services import ProductService


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            return qs
        return qs.filter(is_published=True)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_delete'] = user.has_perm('catalog.can_delete_product')
        context['can_unpublish'] = user.has_perm('catalog.can_unpublish_product')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    context_object_name = 'product'

    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    context_object_name = 'product'

    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return redirect('home')  # или выкинуть 403
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'product'

    login_url = reverse_lazy('login')
    permission_required = 'catalog.can_delete_product'
    raise_exception = True

    def has_permission(self):
        obj = self.get_object()
        return self.request.user == obj.owner or self.request.user.has_perm(self.permission_required)


class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('product_detail', pk=pk)


class ProductsByCategoryView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = ProductService.products_in_category(self.kwargs['pk'])
            cache.set('my_queryset', queryset, 60 * 15)
        return queryset


class ChooseCategoryView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/choose_category.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.order_by('name').values('id', 'name')
        return ctx

