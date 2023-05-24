# metoffice-weather
FarmSetu Take Home Assignment - Backend Engineer

## API Endpoints

API Endpoints
1. Upload Document
Endpoint: /document/
Method: POST
This endpoint allows you to upload a text file containing weather data. The API will parse the data and store it in the database.

2. Get Weather
Endpoint: /temperature/
Method: GET
This endpoint retrieves weather data based on the specified criteria. It supports the following ways to fetch data:

a) For a specific year:

Endpoint: /temperature/?year=<year>
Example: /temperature/?year=2022
b) For a range of years:

Endpoint: /temperature/?start_year=<start_year>&end_year=<end_year>
Example: /temperature/?start_year=2018&end_year=2020
c) Entire weather data in both orders (year order, rank order):

Endpoint: /temperature/
3. Get Summary
Endpoint: /temperature/get-summary
Method: GET
