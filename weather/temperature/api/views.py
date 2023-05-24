from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from media_document.models import Year
from services.temperature import (
    svc_temperature_get_data_for_a_year,
    svc_temperature_get_data_for_range_of_years,
    svc_temperature_get_ordered_data,
    svc_temperature_get_summary,
)


class WeatherDataView(generics.GenericAPIView):
    def get(self, request, **kwargs):
        try:
            if "year" in request.query_params:
                weather_data = svc_temperature_get_data_for_a_year(request.query_params["year"], request.data)
            elif "start_year" in request.query_params or "end_year" in request.query_params:
                start_year = request.query_params.get("start_year")
                end_year = request.query_params.get("end_year")
                weather_data = svc_temperature_get_data_for_range_of_years(start_year, end_year, request.data)
            else:
                weather_data = svc_temperature_get_ordered_data(request.data)

            return Response({"data": weather_data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(
                {"message": f"Invalid Region or Parameter - {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Year.DoesNotExist as e:
            return Response({"message": "Invalid year value"}, status=status.HTTP_400_BAD_REQUEST)


class WeatherDataSummaryView(generics.GenericAPIView):
    def get(self, request, **kwargs):
        try:
            weather_data = svc_temperature_get_summary(request.data)
            return Response({"data": weather_data}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(
                {"message": f"Invalid Region or Parameter - {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
