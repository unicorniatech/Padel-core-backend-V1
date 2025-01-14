from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aprobacion
from .serializers import AprobacionSerializer
from torneos.models import Torneo
from partidos.models import Partido

class AprobacionViewSet(viewsets.ModelViewSet):
    queryset = Aprobacion.objects.all()
    serializer_class = AprobacionSerializer

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        """
        PATCH /api/aprobaciones/<id>/approve/
        Cambia status a 'approved' y crea el Torneo/Partido real en la BD.
        """
        instance = self.get_object()

        if instance.status != 'pending':
            return Response(
                {"detail": "Este registro ya fue procesado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Cambiar status
        instance.status = 'approved'
        instance.save()

        # Crear el registro real, dependiendo del tipo
        if instance.tipo == 'tournament':
            data = instance.data
            torneo = Torneo.objects.create(
                nombre=data['nombre'],
                sede=data['sede'],
                fecha_inicio=data['fecha_inicio'],
                fecha_fin=data['fecha_fin'],
                premio_dinero=data.get('premio_dinero', 0),
                puntos=data.get('puntos', 0),
                imagen_url=data.get('imagen_url', ''),
                tags=data.get('tags', []),
            )
            return Response(
                {"detail": "Torneo creado con éxito", "torneo_id": torneo.id},
                status=status.HTTP_200_OK
            )
        elif instance.tipo == 'match':
            data = instance.data
            partido = Partido.objects.create(
                torneo_id=data['torneo'],
                fecha=data['fecha'],
                hora=data['hora'],
                resultado=data.get('resultado', ''),
            )
            # Asignar equipo_1 y equipo_2
            partido.equipo_1.set(data['equipo_1_ids'])
            partido.equipo_2.set(data['equipo_2_ids'])

            return Response(
                {"detail": "Partido creado con éxito", "partido_id": partido.id},
                status=status.HTTP_200_OK
            )

        return Response({"detail": "Tipo no soportado."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        """
        PATCH /api/aprobaciones/<id>/reject/
        Cambia status a 'rejected', no se crea nada real en la BD.
        """
        instance = self.get_object()

        if instance.status != 'pending':
            return Response(
                {"detail": "Este registro ya fue procesado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.status = 'rejected'
        instance.save()
        return Response(
            {"detail": "Se ha rechazado la aprobación."},
            status=status.HTTP_200_OK
        )
