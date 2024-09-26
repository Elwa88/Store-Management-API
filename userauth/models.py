from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'),
                    ('manager', 'Manager'),
                    ('salesperson', 'Salesperson')]
    role = models.CharField(max_length=11,choices=ROLE_CHOICES, default='salesperson')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    

