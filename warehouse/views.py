from rest_framework import generics
from rest_framework.response import Response
from .models import Category, Product, Supplier, Stock, buying_report
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
    queryset = buying_report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdmin]

class ReportRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = buying_report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdmin]

