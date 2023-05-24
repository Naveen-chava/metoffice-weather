# official lightweight Python image.
FROM python:3.8-slim 

# Copy local code to the container image.
COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
