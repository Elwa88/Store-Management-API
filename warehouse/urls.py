from django.urls import path
from .views import *


urlpatterns = [
    path('category/',CategoryViews.as_view()),
    path('supplier/',SupplierViews.as_view()),
    path('stock/',ListStock.as_view()),
    path('product/',ProductViews.as_view()),
    path('report/',ReportViews.as_view()),
]
