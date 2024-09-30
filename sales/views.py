from rest_framework import generics
from .models import Sale, GenerateReport
from .serializers import SaleSerializer, ReportSerializer
from userauth.permissions import IsAdmin, IsAdminOrReadOnly, IsManager, IsSalesperson


class SaleListCreate(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsSalesperson]

class SaleRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAdminOrReadOnly]
