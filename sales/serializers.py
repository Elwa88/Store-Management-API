from rest_framework import serializers
from .models import Sale, GenerateReport
from warehouse.models import Stock

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'product', 'date_sold', 'client_name', 'client_personal_no','price_sold','quantity_sold','discount']
        read_only_fields = ['discount']

    def validate(self, data):
        quantity_sold = 1
        try :
            quantity_sold = data['quantity_sold']
        except KeyError:
            pass
        product = data['product']
        stock = Stock.objects.get(product_name = product.name)
        if stock.quantity - quantity_sold < 0:
            raise serializers.ValidationError(f"There is only {stock.quantity} {product.name} in stock!")
        
        return data

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
        fields = ['id','sale', 'start_date', 'end_date']