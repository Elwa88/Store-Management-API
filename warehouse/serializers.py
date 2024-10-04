from rest_framework import serializers
from .models import Product, Category, Supplier, Stock, Feedback, GenerateReport

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many = True, read_only = True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','category', 'description', 'buying_date', 'price_bought','price_selling','serial_number','item_code', 'sold']

    def create(self, validated_data):
        stock, created = Stock.objects.get_or_create(product_name = validated_data['name']) 
        product = Product.objects.create(**validated_data)
        stock.quantity+=1
        stock.save()

        return product
    

class FeedbackSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset = Supplier.objects.all())

    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        report = Feedback.objects.create(**validated_data)
        supplier = validated_data['supplier']
        if validated_data['satisfaction'] == 'dissatisfied':
            grade = -validated_data['grade']
        else:
            grade = validated_data['grade']
        supplier.rating += grade
        supplier.save()

        return report
    
class GenerateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerateReport
        fields = "__all__"