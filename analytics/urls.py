from django.urls import path
from .views import GeneralReportView, PerformanceReport

urlpatterns = [
    path('general/',GeneralReportView.as_view()),
    path('performance/<str:users_choice>/', PerformanceReport.as_view())
]
