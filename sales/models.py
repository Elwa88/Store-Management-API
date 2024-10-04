from django.db import models
from warehouse.models import Product
from userauth.models import CustomUser

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_sold = models.DateField(auto_now_add=True)
    client_name = models.CharField(max_length=100)
    client_personal_no = models.CharField(max_length=11, unique=True)
    price_sold = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    salesperson = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)

class GenerateReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
