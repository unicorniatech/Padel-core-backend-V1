from rest_framework import serializers
from .models import Partido
from usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_completo']  # Incluye solo los campos necesarios para los usuarios

class PartidoSerializer(serializers.ModelSerializer):
    # Serializamos los jugadores (usuarios) con su ID y nombre
    equipo_1 = UsuarioSerializer(many=True, read_only=True)
    equipo_2 = UsuarioSerializer(many=True, read_only=True)
    
    # Permitimos que los equipos se envíen como listas de IDs
    equipo_1_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Usuario.objects.all(), write_only=True
    )
    equipo_2_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Usuario.objects.all(), write_only=True
    )

    class Meta:
        model = Partido
        fields = [
            'id', 'torneo', 'equipo_1', 'equipo_2', 'equipo_1_ids', 'equipo_2_ids',
            'fecha', 'hora', 'resultado', 'createdP', 'modifiedP',
        ]

    # Sobrescribimos el método `create` para manejar los ManyToManyFields
    def create(self, validated_data):
        equipo_1_ids = validated_data.pop('equipo_1_ids')
        equipo_2_ids = validated_data.pop('equipo_2_ids')
        partido = Partido.objects.create(**validated_data)
        partido.equipo_1.set(equipo_1_ids)  # Asignamos los IDs al ManyToManyField
        partido.equipo_2.set(equipo_2_ids)
        return partido
