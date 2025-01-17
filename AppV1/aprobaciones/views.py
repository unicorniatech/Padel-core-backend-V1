from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Aprobacion
from .serializers import AprobacionSerializer
from torneos.models import Torneo
from partidos.models import Partido
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AprobacionViewSet(viewsets.ModelViewSet):
    queryset = Aprobacion.objects.all()
    serializer_class = AprobacionSerializer


    def perform_create(self, serializer):
        """
        Se llama automáticamente al hacer POST /api/aprobaciones/.
        Crea el registro Aprobacion en la base de datos y luego envía
        un mensaje al grupo "aprobaciones" para notificar a los WebSockets.
        """
        instance = serializer.save()  # Guardamos la nueva aprobación en la BD

        # 1. Obtener la capa de canales (canal para WS)
        channel_layer = get_channel_layer()
        
        # 2. Preparamos la data a enviar al consumidor
        data = {
            "id": instance.id,
            "tipo": instance.tipo,
            "status": instance.status,
            "detalle": "Se creó una nueva aprobación en estado pending",
        }

        # 3. Usamos group_send para mandar el mensaje a todos los WebSockets
        async_to_sync(channel_layer.group_send)(
            "aprobaciones",  # El mismo nombre que usaste en consumers.py (group_add("aprobaciones", ...))
            {
                "type": "aprobacion_message",  # Debe coincidir con tu método en consumers.py
                "data": data
            }
        )

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
                #tags=data.get('tags', []),
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

            response_data = {"detail": "Partido creado con éxito", "partido_id": partido.id}
        else:
            return Response({"detail": "Tipo no soportado."}, status=status.HTTP_400_BAD_REQUEST)

        # Enviar notificación vía WebSocket diciendo que esta aprobación se aprobó
        channel_layer = get_channel_layer()
        ws_data = {
            "id": instance.id,
            "tipo": instance.tipo,
            "status": instance.status,
            "detalle": "Se aprobó la solicitud"
        }
        async_to_sync(channel_layer.group_send)(
            "aprobaciones",
            {
                "type": "aprobacion_message",
                "data": ws_data
            }
        )

        # Retornar la respuesta HTTP normal
        return Response(response_data, status=status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------
    # (3) Acción para RECHAZAR la aprobación
    # ------------------------------------------------------------------------------------
    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        """
        PATCH /api/aprobaciones/<id>/reject/
        Cambia status a 'rejected', no se crea nada real en la BD.
        Notifica por WebSocket el cambio de estado también.
        """
        instance = self.get_object()

        if instance.status != 'pending':
            return Response(
                {"detail": "Este registro ya fue procesado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Marcamos como rechazado
        instance.status = 'rejected'
        instance.save()

        # Notificar vía WebSocket
        channel_layer = get_channel_layer()
        ws_data = {
            "id": instance.id,
            "tipo": instance.tipo,
            "status": instance.status,
            "detalle": "Se rechazó la solicitud"
        }
        async_to_sync(channel_layer.group_send)(
            "aprobaciones",
            {
                "type": "aprobacion_message",
                "data": ws_data
            }
        )

        return Response(
            {"detail": "Se ha rechazado la aprobación."},
            status=status.HTTP_200_OK
        )