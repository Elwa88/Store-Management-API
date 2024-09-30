from django.urls import path
from .views import SaleListCreate, SaleRetrieve

urlpatterns = [
    path('sale/',SaleListCreate.as_view()),
    path('sale/<int:pk>/',SaleRetrieve.as_view()),
]
