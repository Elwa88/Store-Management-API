from rest_framework.views import APIView
from rest_framework.response import Response
from warehouse.models import Product
from sales.models import Sale
from .serializers import AnalyticsSerializer
from userauth.permissions import IsAdmin


class GeneralReportView(APIView):
    permission_classes = [IsAdmin]

    def post(self,request, *args, **kwargs):
        serializer = AnalyticsSerializer(data = request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = get_end_date(start_date, serializer.validated_data['time_period'])
            sales = Sale.objects.filter(date_sold__range=(start_date, end_date))
            report, total_spent, total_sold = self.generate_report(sales=sales)

            return Response({"Report": report,
                             "Summary" : {
                                    "Total spent" : total_spent,
                                    "Total sold" : total_sold,
                                    "Total profit" : total_sold - total_spent,
                                    },
                        })
        else:
            return Response({"Error" : "Invalid Data!",
                             "valid data example " : {
                                 "time_period" : "choice in (monthly, quarterly, yearly)",
                                 "start_date" : "YYYY-MM-DD",
                             }})
    
    def generate_report(self,sales):
        report = []
        total_spent = 0
        total_sold = 0
        for sale in sales.all():
            product_info = {
                "product" : sale.product.name,
                "bought for" : sale.product.price_bought,
                "sold for" : sale.price_sold,
                "profit" : sale.price_sold - sale.product.price_bought,
                "client info " : {
                    "name" : sale.client_name,
                    "personal number" : sale.client_personal_no
                },
                "date" : sale.date_sold
            }
            total_spent += sale.product.price_bought
            total_sold += sale.price_sold
            report.append(product_info)
        
        return report, total_spent, total_sold
    

class PerformanceReport(APIView):

    permission_classes = [IsAdmin]
    
    def post(self, request, users_choice, *args, **kwargs):
        serializer = AnalyticsSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = get_end_date(start_date, serializer.validated_data['time_period'])
            sales = Sale.objects.filter(date_sold__range = (start_date, end_date)).all()
            match users_choice :
                case "profit_rating":
                    return Response({
                        "Message" : f"This is report generated about top and bottom 5 products by profit in different criterias in {start_date} - {end_date} timeframe",
                        "Report" : self.rate_by_profit(sales)
                    })
                case "turnover_rating":
                    return Response({
                        "Message" : f"This is report generated about top to bottom performing products by turnover in {start_date} - {end_date} timeframe",
                        "Report" : self.rate_by_turnover(sales,start_date,end_date)
                    })
                case "salesmen":
                    return Response({
                        "Message" : f"This is top to bottom performing salespeople {start_date} - {end_date} timeframe",
                        "Report" : self.rete_salespeople(sales)})
        else:
            return Response({"Error" : "Invalid Data!",
                             "valid data example " : {
                                 "time_period" : "choice in (monthly, quarterly, yearly)",
                                 "start_date" : "YYYY-MM-DD",
                             }})
    
    def rate_by_turnover(self,sales,start_date, end_date):

        product_data ={}
        for sale in sales:
            time_to_sell = sale.date_sold - sale.product.buying_date
            if sale.product.name in product_data:
                product_data[sale.product.name]['total_time'] += time_to_sell
                product_data[sale.product.name]['total_discount'] += sale.discount
                product_data[sale.product.name]['sold_products_quantity'] += 1
            else:
                product_data[sale.product.name] = {
                    "total_time" : time_to_sell,
                    "total_discount" : sale.discount,
                    'sold_products_quantity' : 1.0,
                    'overal_grade' : 0
                }
        
        for product_name , data in product_data.items():
            sold_products_qty = Product.objects.filter(buying_date__range =(start_date, end_date), 
                                                       name = product_name, 
                                                       sold = True).count()
            bought_products_qty = Product.objects.filter(buying_date__range=(start_date, end_date),
                                                         name = product_name).count()
            average_time = data['total_time'] / data['sold_products_quantity']
            average_discount = float(data["total_discount"]) / data['sold_products_quantity']
            turnover_ratio = (sold_products_qty / bought_products_qty) * 100
            data['average_time'] = average_time 
            data['average_discount'] = average_discount
            data['turnover_ratio'] =  turnover_ratio 
            data['overal_grade'] += ((-0.2*average_time.days) + (-0.3 * average_discount) + (0.5 * turnover_ratio))

            return [{product_name : {
                "quantity_sold" : data['sold_products_quantity'],
                "average_time" : data['average_time'],
                'average_discount' : f"{(data['average_discount'])}%",
                "turnover_ratio" : float(f"{data['turnover_ratio']:.2f}"),
                'overal_grade' : float(f"{data['overal_grade']:.2f}"),

            }} for product_name, data in sorted(product_data.items(), key=lambda x: x[1]['overal_grade'], reverse=True)]

    def rate_by_profit(self, sales):

        product_data = {}
        for sale in sales:
            profit = sale.price_sold - sale.product.price_bought
            product_name = sale.product.name
            if product_name in product_data:
                product_data[product_name]['total_profit'] += profit
                product_data[product_name]['units_sold'] += 1
            else:
                product_data[product_name] = {
                    "total_profit" : profit,
                    "units_sold" : 1
                }

        for product_name, data in product_data.items():
            if data['units_sold'] > 0:
                data['profit_per_unit'] = data['total_profit'] / data['units_sold']
            else:
                data['profit_per_unit'] = 0

        most_sold_units = sorted(product_data.items(), key=lambda x: x[1]['units_sold'])[-5:]
        least_sold_units = sorted(product_data.items(), key=lambda x: x[1]['units_sold'])[:5]
        most_profit_generated = sorted(product_data.items(), key=lambda x: x[1]['total_profit'])[-5:]
        least_profit_generated = sorted(product_data.items(), key=lambda x: x[1]['total_profit'])[:5]
        most_profit_per_unit = sorted(product_data.items(), key=lambda x: x[1]['profit_per_unit'])[-5:] 
        least_profit_per_unit = sorted(product_data.items(), key=lambda x: x[1]['profit_per_unit'])[:5]
        return {
            "Most Units Sold" : most_sold_units,
            "Least Units Sold" : least_sold_units,
            "Most Profit Generated" : most_profit_generated,
            "Least Profit Generated" : least_profit_generated,
            "Most Profit Per Unit" : most_profit_per_unit,
            "Least Profit Per Unit" : least_profit_per_unit,
        }

    def rete_salespeople(self,sales):
        salesmen_data ={}
        for sale in sales:
            salesman_name = sale.salesperson.first_name + sale.salesperson.last_name
            if salesman_name in salesmen_data:
                salesmen_data[salesman_name]['quantity_sold'] += 1
                salesmen_data[salesman_name]['total_profit_generated'] += sale.price_sold
            else:
                salesmen_data[salesman_name] = {
                    "quantity_sold" : 1,
                    "total_profit_generated" : sale.price_sold
                }
        for _, data in salesmen_data.items():
            data['profit_per_sale'] = data['total_profit_generated'] / data['quantity_sold']

        return sorted(salesmen_data.items(), key=lambda x: x[1]['total_profit_generated'], reverse=True)
    

def get_end_date(start_date, time_period):

    match time_period:
        case 'monthly':
            month = start_date.month + 1
            year = start_date.year
            if month > 12:
                month = 1
                year += 1
        case 'quarterly':
            month = start_date.month + 3
            year = start_date.year
            if month > 12:
                month -= 12
                year += 1
        case 'yearly':
            month = start_date.month 
            year = start_date.year + 1

    return start_date.replace(month = month, year = year)