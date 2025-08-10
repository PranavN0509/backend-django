from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionCreateView, InventoryListView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/', TransactionCreateView.as_view(), name='create-transaction'),
    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
]
