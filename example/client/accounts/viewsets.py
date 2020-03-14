# Create your views here.
from rest_framework import viewsets, permissions

from .models import Profile
from .serializers import ProfileModelSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = ()
    serializer_class = ProfileModelSerializer
