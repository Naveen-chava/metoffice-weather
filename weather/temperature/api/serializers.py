from rest_framework import serializers


class TemperatureSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    jan = serializers.FloatField()
    feb = serializers.FloatField()
    mar = serializers.FloatField()
    apr = serializers.FloatField()
    may = serializers.FloatField()
    jun = serializers.FloatField()
    jul = serializers.FloatField()
    aug = serializers.FloatField()
    sep = serializers.FloatField()
    oct = serializers.FloatField()
    nov = serializers.FloatField()
    dec = serializers.FloatField()
    win = serializers.FloatField()
    spr = serializers.FloatField()
    sum = serializers.FloatField()
    aut = serializers.FloatField()
    ann = serializers.FloatField()


class MonthlyDataSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    year = serializers.IntegerField()


class RankOrderSerializer(serializers.Serializer):
    jan = MonthlyDataSerializer(many=True)
    feb = MonthlyDataSerializer(many=True)
    mar = MonthlyDataSerializer(many=True)
    apr = MonthlyDataSerializer(many=True)
    may = MonthlyDataSerializer(many=True)
    jun = MonthlyDataSerializer(many=True)
    jul = MonthlyDataSerializer(many=True)
    aug = MonthlyDataSerializer(many=True)
    sep = MonthlyDataSerializer(many=True)
    oct = MonthlyDataSerializer(many=True)
    nov = MonthlyDataSerializer(many=True)
    dec = MonthlyDataSerializer(many=True)
    win = MonthlyDataSerializer(many=True)
    spr = MonthlyDataSerializer(many=True)
    sum = MonthlyDataSerializer(many=True)
    aut = MonthlyDataSerializer(many=True)
    ann = MonthlyDataSerializer(many=True)


class SummarySerializer(serializers.Serializer):
    mean = serializers.DecimalField(max_digits=5, decimal_places=2)
    median = serializers.DecimalField(max_digits=5, decimal_places=2)
    min = serializers.DecimalField(max_digits=5, decimal_places=2)
    max = serializers.DecimalField(max_digits=5, decimal_places=2)


class YearSummarySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    monthly_summary = SummarySerializer()
    seasonal_summary = SummarySerializer()
