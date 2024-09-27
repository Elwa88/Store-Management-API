from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               related_name='subcategories')
    def __str__(self):
        return f'{self.name} - Parent : {self.parent if self.parent else None}'
    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(default= 0)
    product_name = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.name} - rating : {self.rating}'
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    buying_date = models.DateField(auto_now_add=True)
    price_bought = models.DecimalField(max_digits=10, decimal_places=2)
    price_selling = models.DecimalField(max_digits=10, decimal_places=2)
    serial_number = models.CharField(max_length=20, unique=True)
    item_code = models.CharField(max_length=5, unique=True)
    
    def __str__(self) -> str:
        return f'{self.category} - {self.name} - code : {self.item_code}'

class Stock(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self) :
        return f'{self.product_name} quantity : {self.quantity}'


class buying_report(models.Model):
    SATISFACTION_CHOICES = [('satisfied', 'Satisfied'),
                            ('neutral', 'Neutral'),
                            ('dissatisfied', 'Dissatisfied')]
    GRADES = [(0,0),
              (1,1),
              (2,2),
              (3,3)]
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete= models.CASCADE)
    satisfaction = models.CharField(max_length=12, choices=SATISFACTION_CHOICES)
    grade = models.PositiveIntegerField(choices=GRADES)
