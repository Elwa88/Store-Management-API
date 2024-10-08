﻿# Store Management API

## Overview

The **Store Management API** is a Django REST Framework (DRF) based application that provides functionality to manage warehouse inventory, track sales, generate analytics, and manage users through authentication. This API is designed to help small and medium-sized businesses efficiently track their products, handle sales transactions, and create periodic reports for performance and profitability.

## Features

- **Warehouse**: Enables users to add and manage products, automatically generating stock to facilitate access and management. Users can manage suppliers through feedback. System provides restocking logic via user input of category and quantity, and automatically orders all products under that category that are below the specified quantity. The system filters suppliers based on ratings for optimal ordering and generates reports about purchases between user-defined dates.
- **Sales**: Allows authorized users to create and manage sales, automatically updating warehouse stock levels based on these sales. Users can also generate reports about sales for user-defined date ranges.
- **Analytics**: Generates general reports about monthly, quarterly, and yearly sales, listing all products sold within a specified timeframe. It calculates the total profit generated, total purchases made for supplying, and the total gross income from sales. Additionally, it provides a detailed performance rating for products that generate the most and least profit, products with the most and least units sold, and a salespeople performance report.
- **User Authentication**: Implements custom role-based registration logic, uses simple JWT authentication system. Provides user permission classes for other applications across the project.

## Endpoints

### **User Authentication Endpoints:**

- **POST** `/api/auth/register/` - Register a new user
- **POST** `/api/auth/token/` - Obtain JWT token (login)
- **POST** `/api/auth/token/refresh/` - Refresh JWT token

### **Warehouse Endpoints:**

- **`/api/warehouse/category/`** - GET: List all categories; POST: Create a new category.
- **`/api/warehouse/category/<int:pk>/`** - GET; PUT; PATCH; DELETE a category.
- **`/api/warehouse/supplier/`** - GET: List all suppliers; POST: Create a new supplier.
- **`/api/warehouse/supplier/<int:pk>/`** - GET; PUT; PATCH; DELETE a supplier.
- **`/api/warehouse/stock/`** - GET: List all stock items.
- **`/api/warehouse/stock/<int:pk>/`** - GET: Retrieve a stock item.
- **`/api/warehouse/product/`** - GET: List all products; POST: Create a new product.
- **`/api/warehouse/product/<int:pk>/`** - GET; PUT; PATCH; DELETE a product.
- **`/api/warehouse/feedback/`** - GET: List all feedback; POST: Create new feedback.
- **`/api/warehouse/feedback/<int:pk>/`** - GET; PUT; PATCH; DELETE feedback.
- **`/api/warehouse/restock/<str:category_name>/<int:stock_quantity>/`** - Enables user to automatically order products under "category_name" which are less than "stock_quantity".
- **`/api/warehouse/generate_report/`** - POST: Generate a report for warehouse analytics.

### **Sales Endpoints:**

- **`/api/sales/sale/`** - GET: List all sales; POST: Create a new sale.
- **`/api/sales/sale/<int:pk>/`** - GET; PUT; PATCH; DELETE a sale.
- **`/api/sales/report/`** - POST: Generate a sales report.

### **Analytics Endpoints:**

- **`/api/analytics/general/`** - GET: Retrieve the general report.
- **`/api/analytics/performance/<str:users_choice>/`** - POST: Generate performance reports based on user’s choice (options: `profit_rating`, `turnover_rating`, `salesmen`).
