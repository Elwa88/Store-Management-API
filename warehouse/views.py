from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Supplier, Stock, Feedback
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer, StockSerializer, FeedbackSerializer, GenerateReportSerializer
from userauth.permissions import IsAdmin, IsAdminOrReadOnly, IsManager


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

class FeedbackListCreate(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdmin]

class FeedbackRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
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

class Report(APIView):
    permission_classes = [IsAdmin]

    def post(self,request,*args, **kwargs):
        serializer = GenerateReportSerializer(data = request.data)
        if serializer.is_valid():
            start_date =serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            category = serializer.validated_data.get('category')
            if category.subcategories.exists():
                return Response({"message":"Enter only non-parent category"})
            
            products = Product.objects.filter(buying_date__range =(start_date, end_date), category = category)
            total = 0
            response = ''
            for product in products.all():
                response += f"{product.name} -- {product.price_bought}$ -- {product.item_code} || "
                total += product.price_bought
            return Response({'report' : f'{response}total = {total}$'})

        else:
            return Response({"message":"Enter valid input. Category - Primary key. Start_date, End_date - YYYY-MM-DD"})