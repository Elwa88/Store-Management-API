from django_filters import rest_framework
from .models import Product, Supplier, Stock

class ProductFilter(rest_framework.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name' : ['exact', 'icontains'],
            'price_bought' : ['exact','lte','gte'],
            'price_selling' : ['exact','lte','gte'],
            'buying_date' : ['exact', 'lte', 'gte'],
            'item_code' : ['exact'],
            'serial_number' : ['exact'],
            'category' : ['exact'],
        }

class SupplierFilter(rest_framework.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'product_name' : ['exact', 'icontains'],
            'rating' : ['gte'],
            'name' : ['exact', 'icontains'],
        }

class StockFilter(rest_framework.FilterSet):
    class Meta:
        model = Stock
        fields = {
            'product_name' : ['exact', 'icontains'],
            'quantity' : ['gte', 'lte']
        }