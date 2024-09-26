from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsAdmin

class UserCreateList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdmin]