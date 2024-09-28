from django.urls import path
from .views import *


urlpatterns = [
    path('category/',CategoriesListCreate.as_view()),
    path('category/<int:pk>/',CategoryRetrieve.as_view()),
    path('supplier/',SuppliersListCreate.as_view()),
    path('supplier/<int:pk>/',SupplierRetrieve.as_view()),
    path('stock/',StockList.as_view()),
    path('stock/<int:pk>/',StockRetrieve.as_view()),
    path('product/',ProductsListCreate.as_view()),
    path('product/<int:pk>/',ProductRetrieve.as_view()),
    path('report/',ReportListCreate.as_view()),
    path('report/<int:pk>/',ReportRetrieve.as_view()),
    path('restock/<str:category_name>/<int:stock_quantity>/',Restock.as_view())
]
