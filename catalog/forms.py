from django import forms
from .models import Product
from django.core.exceptions import ValidationError

banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        description = cleaned_data.get('description', '')

        for word in banned_words:
            if word in name.lower():
                self.add_error('name', f'Название содержит запрещённое слово: {word}')
            if word in description.lower():
                self.add_error('description', f'Описание содержит запрещённое слово: {word}')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название продукта'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })

        self.fields['category'].empty_label = 'Выберите категорию'

        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену'
        })
