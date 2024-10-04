from rest_framework import serializers
from .models import Sale, GenerateReport
from warehouse.models import Stock

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'product', 'date_sold', 'client_name', 'client_personal_no','price_sold','discount','salesperson']
        read_only_fields = ['discount','salesperson']

    def validate(self, data):
        product = data['product']
        stock = Stock.objects.get(product_name = product.name)
        if stock.quantity - 1 < 0:
            raise serializers.ValidationError(f"Item out of stock!")
        
        return data

    def create(self, validated_data):
        sale = Sale.objects.create(**validated_data)
        product = validated_data['product']
        stock = Stock.objects.get(product_name = product.name)
        discount = product.price_selling - sale.price_sold
        product.sold = True
        product.save()
        sale.discount = discount
        sale.save()
        stock.quantity -= 1
        stock.save()
        
        return sale
    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateReport
        fields = ['id', 'start_date', 'end_date']