from rest_framework import serializers
from .models import Sale, GenerateReport
from warehouse.models import Stock

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['product', 'date_sold', 'client_name', 'client_personal_no','price_sold','quantity_sold','discount']
        read_only_fields = ['discount']

    def create(self, validated_data):
        sale = Sale.objects.create(**validated_data)
        product = validated_data['product']
        stock = Stock.objects.get(product_name = product.name)
        discount = product.price_selling - sale.price_sold
        sale.discount = discount
        sale.save()
        stock.quantity -= sale.quantity_sold
        stock.save()
        
        return sale
    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateReport
        fields = ['sale', 'start_date', 'end_date']