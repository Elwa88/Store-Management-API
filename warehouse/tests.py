from django.test import TestCase
from .models import Product, Category, Stock, Supplier
from rest_framework import status
from rest_framework.test import APIClient
from userauth.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class CategorySupplierStockTests(TestCase):
    def setUp(self) :
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create(username='user_admin',password = 'userpass', first_name ='name', last_name = "lname", role = 'admin')
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.manager_user = CustomUser.objects.create(username='user_manager',password = 'userpass', first_name ='name', last_name = "lname", role = 'manager')
        self.manager_token = RefreshToken.for_user(self.manager_user)
        self.salesperson_user = CustomUser.objects.create(username='user_salesperson',password = 'userpass', first_name ='name', last_name = "lname", role = 'salesperson')
        self.salesperson_token = RefreshToken.for_user(self.salesperson_user)

    def test_category_views_admin_auth(self):

        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.admin_token.access_token}')
        response = self.client.post('/api/warehouse/category/',{'name' : "category1"})
        response1 = self.client.get('/api/warehouse/category/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.patch('/api/warehouse/category/1/', {'name' : 'category2'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_category_views_other_auth(self):
        #for salespeople
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.salesperson_token.access_token}')
        response = self.client.get('/api/warehouse/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response1 = self.client.post('/api/warehouse/category/',{'name' : "category1"})
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
        response2 = self.client.patch('/api/warehouse/category/1/', {'name' : 'category2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #for managers
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.manager_token.access_token}')
        response = self.client.get('/api/warehouse/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response1 = self.client.post('/api/warehouse/category/',{'name' : "category1"})
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
        response2 = self.client.patch('/api/warehouse/category/1/', {'name' : 'category2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_supplier_views_admin_auth(self):

        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.admin_token.access_token}')
        response = self.client.post('/api/warehouse/supplier/',{'name' : "supplier1", "email" : "supplier@test.email", "product_name" : "product1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response1 = self.client.get('/api/warehouse/supplier/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.patch('/api/warehouse/supplier/1/', {'name' : 'supplier2'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
    
    def test_supplier_views_other_auth(self):
        #for salespeople
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.salesperson_token.access_token}')
        response = self.client.post('/api/warehouse/supplier/',{'name' : "supplier1", "email" : "supplier@test.email", "product_name" : "product1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response1 = self.client.get('/api/warehouse/supplier/')
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
        response2 = self.client.patch('/api/warehouse/supplier/1/', {'name' : 'supplier2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        #for managers
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.manager_token.access_token}')
        response = self.client.post('/api/warehouse/supplier/',{'name' : "supplier1", "email" : "supplier@test.email", "product_name" : "product1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response1 = self.client.get('/api/warehouse/supplier/')
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
        response2 = self.client.patch('/api/warehouse/supplier/1/', {'name' : 'supplier2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_stock_views_admin_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.admin_token.access_token}')
        response = self.client.post('/api/warehouse/stock/',{'product_name' : "product1", "quantity" : 3})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response1 = self.client.get('/api/warehouse/stock/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        stock = Stock.objects.create(**{"product_name" : "product1",
                                        "quantity" : 4})
        response2 = self.client.patch('/api/warehouse/stock/1/', {'product_name' : 'product2'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_stock_views_other_auth(self):
        # for salespeople
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.salesperson_token.access_token}')
        response = self.client.post('/api/warehouse/stock/',{'product_name' : "product1", "quantity" : 3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response1 = self.client.get('/api/warehouse/stock/')
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

        stock = Stock.objects.create(**{"product_name" : "product1",
                                        "quantity" : 4})
        
        response2 = self.client.patch('/api/warehouse/stock/1/', {'product_name' : 'product2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        # for managers
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.manager_token.access_token}')
        response = self.client.post('/api/warehouse/stock/',{'product_name' : "product1", "quantity" : 3})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response1 = self.client.get('/api/warehouse/stock/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        stock = Stock.objects.create(**{"product_name" : "product1",
                                        "quantity" : 4})
        
        response2 = self.client.patch('/api/warehouse/stock/1/', {'product_name' : 'product2'})
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

class ProductFeedbackTests(TestCase):
    def setUp(self) :
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create(username='user_admin',password = 'userpass', first_name ='name', last_name = "lname", role = 'admin')
        self.admin_token = RefreshToken.for_user(self.admin_user)
        self.manager_user = CustomUser.objects.create(username='user_manager',password = 'userpass', first_name ='name', last_name = "lname", role = 'manager')
        self.manager_token = RefreshToken.for_user(self.manager_user)
        self.salesperson_user = CustomUser.objects.create(username='user_salesperson',password = 'userpass', first_name ='name', last_name = "lname", role = 'salesperson')
        self.salesperson_token = RefreshToken.for_user(self.salesperson_user)

    def test_product_views_admin_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.admin_token.access_token}')
        category = Category.objects.create(**{"name" : "category1"})
        self.assertEqual(len(Stock.objects.all()), 0)
        response = self.client.post('/api/warehouse/product/',{
                                                                "id": 1,
                                                                "category": category.id,
                                                                "name": "product1",
                                                                "description": "descr.",
                                                                "price_bought": "25.00",
                                                                "price_selling": "40.00",
                                                                "serial_number": "SN123456",
                                                                "item_code": "ITEM1",
                                                            })
        self.product = Product.objects.get(pk = 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stock = Stock.objects.get(product_name = "product1")
        self.assertEqual(stock.quantity, 1)
        response2 = self.client.get('/api/warehouse/product/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertLess(self.product.price_selling, 49)
        response3 = self.client.patch('/api/warehouse/product/1/',{"price_selling": "50.00"})
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertGreater(self.product.price_selling, 49)
        response4 = self.client.delete('/api/warehouse/product/1/')
        self.assertEqual(response4.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_views_other_auth(self):
        category = Category.objects.create(**{"name" : "category1"})
        product = Product.objects.create(**{
                                    "id": 1,
                                    "category": category,
                                    "name": "product1",
                                    "description": "descr.",
                                    "price_bought": "25.00",
                                    "price_selling": "40.00",
                                    "serial_number": "SN123456",
                                    "item_code": "ITEM1",
                                })
        #for salespeople
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.salesperson_token.access_token}')
        response = self.client.post('/api/warehouse/product/',{
                                                                "id": 1,
                                                                "category": category.id,
                                                                "name": "product1",
                                                                "description": "descr.",
                                                                "price_bought": "25.00",
                                                                "price_selling": "40.00",
                                                                "serial_number": "SN123456",
                                                                "item_code": "ITEM1",
                                                            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response2 =self.client.get('/api/warehouse/product/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get('/api/warehouse/product/1/')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        response4 = self.client.delete('/api/warehouse/product/1/')
        self.assertEqual(response4.status_code, status.HTTP_403_FORBIDDEN)

        #for managers
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.manager_token.access_token}')
        response = self.client.post('/api/warehouse/product/',{
                                                                "id": 1,
                                                                "category": category.id,
                                                                "name": "product1",
                                                                "description": "descr.",
                                                                "price_bought": "25.00",
                                                                "price_selling": "40.00",
                                                                "serial_number": "SN123456",
                                                                "item_code": "ITEM1",
                                                            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response2 =self.client.get('/api/warehouse/product/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get('/api/warehouse/product/1/')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        response4 = self.client.delete('/api/warehouse/product/1/')
        self.assertEqual(response4.status_code, status.HTTP_403_FORBIDDEN)

    def test_feedback_views_admin_auth(self):
        category = Category.objects.create(**{"name" : "category1"})
        product = Product.objects.create(**{
                                    "id": 1,
                                    "category": category,
                                    "name": "product1",
                                    "description": "descr.",
                                    "price_bought": "25.00",
                                    "price_selling": "40.00",
                                    "serial_number": "SN123456",
                                    "item_code": "ITEM1",
                                })
        supplier = Supplier.objects.create(**{"name" : "supplier1", "email" : "supplier@email.test", "product_name" : "product1", "rating" : 5})
        self.assertEqual(supplier.rating, 5)

        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.admin_token.access_token}')
        response = self.client.post('/api/warehouse/feedback/', {"id" : 1, "product" : product.id , "supplier" : supplier.id, "satisfaction" : "satisfied", "grade" : 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        supplier.refresh_from_db()
        self.assertEqual(supplier.rating,7)
        response1 = self.client.get('/api/warehouse/feedback/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
