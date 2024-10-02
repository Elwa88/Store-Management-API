from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Sale, GenerateReport
from .serializers import SaleSerializer, ReportSerializer
from userauth.permissions import IsAdminOrReadOnly, IsSalesperson


class SaleListCreate(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsSalesperson]

class SaleRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReportViews(APIView):

    def post(self, request, *args, **kwargs):

        serializer = ReportSerializer(data = request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            sales = Sale.objects.filter(date_sold__range =(start_date, end_date))
            sold_products = []
            report = ''
            profit = 0
            product_list = []
            
            for sale in sales.all():
                sold_products.append((sale.product, sale.price_sold))

            for i in sold_products:
                product_info = {
                    "name" : i[0].name,
                    "bought for" : i[0].price_bought,
                    "sold for" : i[1],
                    "profit" : i[1] - i[0].price_bought
                }
                product_list.append(product_info)
                profit += i[1] - i[0].price_bought

            return Response({"report": product_list,
                             "total profit" : profit})
        else:
            return Response({"Error" : "Invalid data inputed!"})