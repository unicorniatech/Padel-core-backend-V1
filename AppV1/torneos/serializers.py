from rest_framework import serializers
from .models import Torneo

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'
    def validate_tags(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("No puedes seleccionar más de 3 tags.")
        tags_nombres = [tag.nombre for tag in value]
        if "Amateur" in tags_nombres and "Profesional" in tags_nombres:
            raise serializers.ValidationError('No puedes seleccionar "Amateur" y "Profesional" al mismo tiempo.')

        return value
