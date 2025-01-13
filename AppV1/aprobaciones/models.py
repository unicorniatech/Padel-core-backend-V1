from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.
class PendingApproval(models.Model):
    TIPO_CHOICES = (
        ('tournament', 'Tournament'),
        ('match', 'Match'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Aquí se guarda la información que luego se usará para crear
    # un torneo o partido real. Puede ser un JSON con cualquier estructura.
    data = models.JSONField()
    
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} - {self.status} - creado {self.created_at}"