from rest_framework import serializers
from .models import Naver, Weather_api


class NaverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naver
        # fields = '__all__'
        exclude = 'description, telephone,'
        

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather_api
        fields = ('id', 'location', 'weather_summary', 'now_temp', 'dust', 'little_dust',)        