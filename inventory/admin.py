from django.contrib import admin
from .models import Product, StockMain, StockDetail

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'unit']
    search_fields = ['name', 'sku']

@admin.register(StockMain)
class StockMainAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'reference', 'date']
    list_filter = ['transaction_type']
    search_fields = ['reference']

@admin.register(StockDetail)
class StockDetailAdmin(admin.ModelAdmin):
    list_display = ['stock', 'product', 'quantity']
    list_filter = ['product']
