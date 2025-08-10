from django.db import models


class Product(models.Model):  # prodmast
    name = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class StockMain(models.Model):  # stckmain
    TRANSACTION_TYPES = [('IN', 'Stock In'), ('OUT', 'Stock Out')]
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference} on {self.date.strftime('%Y-%m-%d')}"


class StockDetail(models.Model):  # stckdetail
    stock = models.ForeignKey(StockMain, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"