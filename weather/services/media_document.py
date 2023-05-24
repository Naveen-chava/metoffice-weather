import pandas as pd

from io import StringIO
from django.db import transaction

from media_document.models import MonthlyTemperature, SeasonalTemperature, Year
from common.constants import Region, Parameter


def _validate_temp_value(temperature):
    try:
        temperature = float(temperature)
    except ValueError:
        temperature = None

    return temperature


def svc_media_document_add_data_to_db(df, region, parameter):
    with transaction.atomic():
        for index, row in df.iterrows():
            year = row["year"]

            months = row.index[1:13]  # all the month columns

            seasons = row.index[13:17]  # all the season columns

            annual_temp = row["ann"]

            ann = _validate_temp_value(annual_temp)

            yearly_temp = Year.objects.create(year=year, annual_temperature=ann, region=region, parameter=parameter)

            for month in months:
                temperature = _validate_temp_value(row[month])
                monthly_temp = MonthlyTemperature.objects.create(
                    year=yearly_temp, month=month, temperature=temperature
                )

            for season in seasons:
                temperature = _validate_temp_value(row[season])
                seasonal_temp = SeasonalTemperature.objects.create(
                    year=yearly_temp, season=season, temperature=temperature
                )


def svc_media_document_process_the_text_file(request_data: dict) -> None:
    if "file_name" not in request_data:
        raise ValueError("Missing file_name")
    if "region" not in request_data:
        raise ValueError("Missing region")
    if "parameter" not in request_data:
        raise ValueError("Missing parameter")

    file_obj = request_data["file_name"].open()
    region = request_data["region"]
    parameter = request_data["parameter"]

    region = Region.get_obj_for_string(region)
    parameter = Parameter.get_obj_for_string(parameter)

    file_content = file_obj.read().decode("utf-8")

    # reading the text file as pandas dataframe.
    # https://stackoverflow.com/questions/67196527/pandas-read-text-file-slicing-columns-possibly-with-empty-strings-values-accordi
    df = pd.read_fwf(StringIO(file_content), skiprows=5, keep_default_na=False)

    svc_media_document_add_data_to_db(df, region, parameter)
