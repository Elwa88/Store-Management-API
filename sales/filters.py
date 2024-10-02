from django_filters import rest_framework
from .models import Sale

class SaleFilter(rest_framework.FilterSet):
    class Meta:
        model = Sale
        fields = {
            "product" : ['exact'],
            "client_name" : ['exact','icontains'],
            "client_personal_no" : ['exact'],
        }