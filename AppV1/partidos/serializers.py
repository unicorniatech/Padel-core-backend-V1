from rest_framework import serializers
from .models import Partido

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

    def validate(self, data):
        if data['equipo_1'] == data['equipo_2']:
            raise serializers.ValidationError("Los equipos no pueden ser iguales.")
        return data
