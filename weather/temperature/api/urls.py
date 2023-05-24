from django.urls import path
from . import views

app_name = "temperature"

urlpatterns = [
    path("", views.WeatherDataView.as_view(), name="handler-weather-data"),
    path("get-summary", views.WeatherDataSummaryView.as_view(), name="handler-weather-data-summary"),
]
