from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import * 

@api_view(['GET'])
def cita_list(request):
    citas = Cita.objects.all()
    serializer=CitaSerializer(citas,many=True)
    return Response(serializer.data)