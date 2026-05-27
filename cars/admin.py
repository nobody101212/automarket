from django.contrib import admin
from .models import Brand, CarModel, Car, CarImage, Review


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name']
    list_filter = ['brand']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'seller', 'price', 'city', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'brand', 'condition', 'transmission']
    search_fields = ['brand__name', 'model__name', 'seller__username']
    inlines = [CarImageInline]
    list_editable = ['is_active', 'is_featured']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['car', 'user', 'rating', 'created_at']