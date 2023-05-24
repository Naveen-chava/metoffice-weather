from django.db import models

from common.constants import Region, Parameter


class Year(models.Model):
    year = models.PositiveIntegerField()
    annual_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    region = models.PositiveIntegerField(choices=Region.get_choices())
    parameter = models.PositiveIntegerField(choices=Parameter.get_choices())

    def __str__(self):
        return str(self.year)

    class Meta:
        unique_together = ["region", "parameter", "year"]


class MonthlyTemperature(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    month = models.CharField(max_length=3)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.year} - {self.month}"


class SeasonalTemperature(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    season = models.CharField(max_length=3)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.year} - {self.season}"
