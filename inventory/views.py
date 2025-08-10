from rest_framework import viewsets, generics
from .models import Product, StockMain
from .serializers import ProductSerializer, StockMainSerializer, InventorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


class StockMainViewSet(viewsets.ModelViewSet):
    queryset = StockMain.objects.prefetch_related('stockdetail_set').all().order_by('-date')
    serializer_class = StockMainSerializer


@api_view(['GET'])
def inventory_view(request):
    from .models import StockDetail, Product
    inventory = []

    for product in Product.objects.all():
        stock_in = StockDetail.objects.filter(
            product=product, stock__transaction_type='IN'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        stock_out = StockDetail.objects.filter(
            product=product, stock__transaction_type='OUT'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        available = stock_in - stock_out

        inventory.append({
            "product": product.name,
            "sku": product.sku,
            "quantity_available": available,
            "unit": product.unit
        })

    return Response(inventory, status=status.HTTP_200_OK)


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = StockMainSerializer


class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return Product.objects.all()