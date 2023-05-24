from typing import Union

from django.db.models import Avg, Max, Min
from statistics import median

from common.constants import Region, Parameter
from common.constants import (
    WEATHER_DATA_SCHEMA,
    MONTHS,
    SEASONS,
    YEAR,
    RANK_ORDER,
    YEAR_ORDER,
)
from common.mapping import months_mapping, seasons_mapping
from media_document.models import Year, MonthlyTemperature, SeasonalTemperature
from temperature.api.serializers import TemperatureSerializer, RankOrderSerializer, YearSummarySerializer


def _validate_region_and_parameter(request_data: dict) -> Union[Region, Parameter]:
    if "region" not in request_data:
        raise ValueError("Missing region")
    if "parameter" not in request_data:
        raise ValueError("Missing parameter")

    region = Region.get_obj_for_string(request_data["region"])
    parameter = Parameter.get_obj_for_string(request_data["parameter"])

    return region, parameter


def _build_weather_data_dict(year: Year) -> dict:  #  region: Region, parameter: Parameter
    weather_data_dict = WEATHER_DATA_SCHEMA.copy()  # deep copying the object

    # throws DoesNotExist error
    # year = Year.objects.get(year=year, region=region, parameter=parameter)
    annual_temperature = year.annual_temperature

    monthly_temperatures = MonthlyTemperature.objects.filter(year=year)

    seasonal_temperatures = SeasonalTemperature.objects.filter(year=year)

    weather_data_dict["year"] = year.year
    weather_data_dict["ann"] = annual_temperature

    for month in monthly_temperatures:
        if month.month in months_mapping:
            weather_data_dict[months_mapping[month.month]] = month.temperature

    for season in seasonal_temperatures:
        if season.season in seasons_mapping:
            weather_data_dict[seasons_mapping[season.season]] = season.temperature

    return weather_data_dict


def svc_temperature_get_data_for_a_year(year: int, request_data: dict) -> dict:
    region, parameter = _validate_region_and_parameter(request_data)

    # throws DoesNotExist error
    year = Year.objects.get(year=year, region=region, parameter=parameter)

    weather_data = _build_weather_data_dict(year)

    return TemperatureSerializer(weather_data, many=False).data


def svc_temperature_get_data_for_range_of_years(start_year: int, end_year: int, request_data: dict) -> dict:
    if not start_year:
        raise ValueError("Missing start_year")
    if not end_year:
        raise ValueError("Missing end_year")
    if start_year >= end_year:
        raise ValueError("start_year should be less than end_year")

    region, parameter = _validate_region_and_parameter(request_data)

    # def svc_get_data_for_range_of_years(start_year, end_year, region, parameter):

    years_data = []
    years = Year.objects.filter(region=region, parameter=parameter, year__range=(start_year, end_year))

    for year in years:
        weather_data = _build_weather_data_dict(year)

        years_data.append(weather_data)

    weather_data_serialized = TemperatureSerializer(years_data, many=True)

    return weather_data_serialized.data


def _get_year_ordered_data(region: Region, parameter: Parameter) -> dict:
    years_data = []
    years = Year.objects.filter(region=region, parameter=parameter)

    for year in years:
        weather_data = _build_weather_data_dict(year)

        years_data.append(weather_data)

    weather_data_serialized = TemperatureSerializer(years_data, many=True)

    return weather_data_serialized.data


def _get_rank_ordered_data(region: Region, parameter: Parameter) -> dict:
    weather_data_dict = WEATHER_DATA_SCHEMA.copy()

    for month in MONTHS:
        monthly_data = []
        monthly_temperatures = MonthlyTemperature.objects.filter(
            year__region=region, year__parameter=parameter, month=month
        ).order_by("-temperature")

        for month in monthly_temperatures:
            monthly_data.append({"temperature": month.temperature, "year": month.year.year})

        if month.month in months_mapping:
            weather_data_dict[months_mapping[month.month]] = monthly_data

    for season in SEASONS:
        seasonal_data = []
        seasonal_temperatures = SeasonalTemperature.objects.filter(
            year__region=region, year__parameter=parameter, season=season
        ).order_by("-temperature")

        for season in seasonal_temperatures:
            seasonal_data.append({"temperature": season.temperature, "year": season.year.year})

        if season.season in seasons_mapping:
            weather_data_dict[seasons_mapping[season.season]] = seasonal_data

    years_data = []
    yearly_temperatures = Year.objects.filter(region=region, parameter=parameter).order_by("-annual_temperature")

    for year in yearly_temperatures:
        years_data.append({"temperature": year.annual_temperature, "year": year.year})

    weather_data_dict[YEAR] = years_data

    return RankOrderSerializer(weather_data_dict).data


def svc_temperature_get_ordered_data(request_data: dict) -> dict:
    region, parameter = _validate_region_and_parameter(request_data)

    if "ordering" not in request_data:
        raise ValueError("Missing ordering")

    ordering = request_data["ordering"].upper()

    if (ordering != RANK_ORDER) and (ordering != YEAR_ORDER):
        raise ValueError(f"Invalid ordering. Available options {RANK_ORDER, YEAR_ORDER}")

    if ordering == YEAR_ORDER:
        return _get_year_ordered_data(region, parameter)
    else:
        return _get_rank_ordered_data(region, parameter)


def _get_monthly_summary_for_a_year(year: Year):
    monthly_temperatures = MonthlyTemperature.objects.filter(year=year)
    monthly_temperatures = monthly_temperatures.exclude(temperature=None)

    mean_temp = monthly_temperatures.aggregate(avg_temp=Avg("temperature"))["avg_temp"]

    # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
    temps = list(monthly_temperatures.values_list("temperature", flat=True))
    median_temp = median(temps)

    min_temp = monthly_temperatures.aggregate(min_temp=Min("temperature"))["min_temp"]

    max_temp = monthly_temperatures.aggregate(max_temp=Max("temperature"))["max_temp"]

    return {"min": min_temp, "max": max_temp, "mean": mean_temp, "median": median_temp}


def _get_seasonal_summary_for_a_year(year: Year):
    seasonal_temperatures = SeasonalTemperature.objects.filter(year=year)
    seasonal_temperatures = seasonal_temperatures.exclude(temperature=None)

    mean_temp = seasonal_temperatures.aggregate(avg_temp=Avg("temperature"))["avg_temp"]

    # https://stackoverflow.com/questions/37205793/django-values-list-vs-values
    temps = list(seasonal_temperatures.values_list("temperature", flat=True))
    median_temp = median(temps)

    min_temp = seasonal_temperatures.aggregate(min_temp=Min("temperature"))["min_temp"]

    max_temp = seasonal_temperatures.aggregate(max_temp=Max("temperature"))["max_temp"]

    return {"min": min_temp, "max": max_temp, "mean": mean_temp, "median": median_temp}


def svc_temperature_get_summary(request_data: dict) -> dict:
    region, parameter = _validate_region_and_parameter(request_data)

    years = Year.objects.filter(region=region, parameter=parameter)

    weather_summary = []

    for year in years:
        yearly_data = {}
        yearly_data["year"] = year.year

        monthly_data = _get_monthly_summary_for_a_year(year)
        yearly_data["monthly_summary"] = monthly_data

        seasonal_data = _get_seasonal_summary_for_a_year(year)
        yearly_data["seasonal_summary"] = seasonal_data

        weather_summary.append(yearly_data)

    return YearSummarySerializer(weather_summary, many=True).data
