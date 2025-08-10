from rest_framework import serializers
from .models import Product, StockMain, StockDetail
from django.db import transaction
from django.db.models import Sum

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters.")
        return value

    def validate_sku(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("SKU must be at least 2 characters.")
        return value


class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetail
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class StockMainSerializer(serializers.ModelSerializer):
    details = StockDetailSerializer(many=True)

    class Meta:
        model = StockMain
        fields = ['transaction_type', 'reference', 'details']

    @transaction.atomic
    def create(self, validated_data):
        details = validated_data.pop('details')
        stock = StockMain.objects.create(**validated_data)

        for detail in details:
            StockDetail.objects.create(stock=stock, **detail)

        return stock



class InventorySerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'unit', 'stock']

    def get_stock(self, product):

        ins = StockDetail.objects.filter(product=product, stock__transaction_type='IN').aggregate(total=Sum('quantity'))['total'] or 0

        outs = StockDetail.objects.filter(product=product, stock__transaction_type='OUT').aggregate(total=Sum('quantity'))['total'] or 0

        return ins - outs