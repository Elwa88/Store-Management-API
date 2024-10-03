from django.urls import path
from .views import GeneralReportView

urlpatterns = [
    path('general/',GeneralReportView.as_view())
]
