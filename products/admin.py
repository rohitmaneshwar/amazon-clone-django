from django.contrib import admin
from .models import Category, Product

# Admin panel me Category dikhane ke liye
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Admin panel me Product ko achhe se list karne ke liye
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)