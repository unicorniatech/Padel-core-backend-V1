from rest_framework import viewsets
from .models import Torneo
from .serializers import TorneoSerializer

class TorneoViewSet(viewsets.ModelViewSet):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer


#from django.shortcuts import render

# Create your views here.
#from rest_framework import viewsets
#from .models import Torneo
#from .serializers import TorneoSerializer

#class TorneoViewSet(viewsets.ModelViewSet):
#    queryset = Torneo.objects.all()
#    serializer_class = TorneoSerializer