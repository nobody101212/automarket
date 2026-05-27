from django import forms
from .models import Car, CarImage, Review, Brand, CarModel
from datetime import datetime


class SearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Марка, модель...', 'class': 'search-input'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, empty_label='Все марки', widget=forms.Select(attrs={'class': 'filter-select'}))
    price_from = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Цена от', 'class': 'filter-input'}))
    price_to = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Цена до', 'class': 'filter-input'}))
    year_from = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Год от', 'class': 'filter-input'}))
    year_to = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Год до', 'class': 'filter-input'}))
    condition = forms.ChoiceField(choices=[('', 'Состояние')] + list(Car.CONDITION_CHOICES), required=False, widget=forms.Select(attrs={'class': 'filter-select'}))
    transmission = forms.ChoiceField(choices=[('', 'КПП')] + list(Car.TRANSMISSION_CHOICES), required=False, widget=forms.Select(attrs={'class': 'filter-select'}))
    fuel_type = forms.ChoiceField(choices=[('', 'Топливо')] + list(Car.FUEL_CHOICES), required=False, widget=forms.Select(attrs={'class': 'filter-select'}))


class CarForm(forms.ModelForm):
    CURRENT_YEAR = datetime.now().year
    YEAR_CHOICES = [(y, y) for y in range(CURRENT_YEAR, 1960, -1)]
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        exclude = ['seller', 'views_count', 'created_at', 'updated_at', 'is_active', 'is_featured']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control', 'id': 'id_brand'}),
            'model': forms.Select(attrs={'class': 'form-control', 'id': 'id_model'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в сомах'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Пробег в км'}),
            'engine_volume': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2.0', 'step': '0.1'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'drive': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+996 XXX XXX XXX'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Бишкек'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }