from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status,viewsets
from .models import User
from .serializers import UserSerializer
from django.utils.translation import activate


class UserViewSet(viewsets.ModelViewSet):
    activate('ar')
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()