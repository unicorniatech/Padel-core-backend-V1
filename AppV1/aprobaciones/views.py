from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PendingApproval
from .serializers import PendingApprovalSerializer
from torneos.models import Torneo
from partidos.models import Partido
from usuarios.models import Usuario
# Create your views here.
class PendingApprovalViewSet(viewsets.ModelViewSet):
    queryset = PendingApproval.objects.all()
    serializer_class = PendingApprovalSerializer

    # POST /api/pendientes/ -> Crea un PendingApproval con la data que mandes (status=pending)
    # GET /api/pendientes/ -> Lista todos (o filtra)
    # PATCH/PUT /api/pendientes/<id>/ -> Actualiza un PendingApproval

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        """
        Endpoint personalizado para aprobar el PendingApproval y
        crear el torneo o partido real en la base de datos de PostgreSQL.
        """
        instance = self.get_object()
        if instance.status != 'pending':
            return Response(
                {"detail": "Este registro ya fue procesado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1) Cambiar status a 'approved'
        instance.status = 'approved'
        instance.save()

        # 2) Leer el tipo y la data
        tipo = instance.tipo
        data = instance.data  # Dict con los campos que guardaste

        if tipo == 'tournament':
            # Crear el torneo usando la data
            torneo = Torneo.objects.create(
                nombre=data['nombre'],
                sede=data['sede'],
                fecha_inicio=data['fecha_inicio'],
                fecha_fin=data['fecha_fin'],
                premio_dinero=data.get('premio_dinero', 0),
                puntos=data.get('puntos', 0),
                imagen_url=data.get('imagen_url', ''),
                tags=data.get('tags', []),  # Asumiendo que tu model Torneo maneje tags = ArrayField
            )
            # Si todo salió bien, devuelves algún mensaje o el torneo creado
            return Response(
                {"detail": "Aprobado y Torneo creado", "torneo_id": torneo.id},
                status=status.HTTP_200_OK
            )

        elif tipo == 'match':
            # Crear el partido usando la data
            # Recuerda que tu Partido requiere:
            # torneo (ID)
            # fecha
            # hora
            # resultado (opcional)
            # equipo_1 (m2m) -> se asigna luego
            # equipo_2 (m2m) -> se asigna luego
            partido = Partido.objects.create(
                torneo_id=data['torneo'],
                fecha=data['fecha'],
                hora=data['hora'],
                resultado=data.get('resultado', ''),
            )
            # Asignar many-to-many: equipo_1 y equipo_2
            partido.equipo_1.set(data['equipo_1_ids'])
            partido.equipo_2.set(data['equipo_2_ids'])

            return Response(
                {"detail": "Aprobado y Partido creado", "partido_id": partido.id},
                status=status.HTTP_200_OK
            )

        # Si no coincide con nada, devuelves un error
        return Response(
            {"detail": "Tipo no soportado."},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        """
        Endpoint personalizado para rechazar el PendingApproval.
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