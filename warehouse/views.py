from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Supplier, Stock, BuyingReport
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer, StockSerializer, ReportSerializer
from userauth.permissions import IsAdmin, IsAdminOrReadOnly, IsManager, IsSalesperson


class CategoriesListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class SuppliersListCreate(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdmin]

class SupplierRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdmin] 

class StockList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsManager]

class StockRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductsListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReportListCreate(generics.ListCreateAPIView):
    queryset = BuyingReport.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdmin]

class ReportRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuyingReport.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdmin]


class Restock(APIView):
    def get(self, request, category_name, stock_quantity, *args, **kwargs):
        category = Category.objects.get(name = category_name)

        if category.subcategories.exists():
            return Response({"message" : "plaese enter only non-parent category"})  
         
        else:
            products = Stock.objects.filter(product_name__icontains=category_name, quantity__lt = stock_quantity)
            supplier = Supplier.objects.filter(product_name = category_name).order_by('-rating')[:1]
            for product in products:
                return Response({"message":f"ordered {5 - product.quantity} {product.product_name} from {supplier[0].name}"})
            