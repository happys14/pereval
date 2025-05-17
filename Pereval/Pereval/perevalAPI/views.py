from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    User,
    Coordinates,
    Level,
    Images,
    SpecificationOfPereval,
)
from .serializers import (
    UserSerializer,
    SpecificationOfPerevalSerializer,
    CoordinatesSerializer,
    LevelSerializer,
    ImagesSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordinatesViewSet(viewsets.ModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinatesSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class SpecificationOfPerevalViewSet(viewsets.ModelViewSet):
    queryset = SpecificationOfPereval.objects.all()
    serializer_class = SpecificationOfPerevalSerializer
    filterset_fields = ['user__email']

    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status != 'new':
            return Response({
                "state": 0,
                "message": "Описание уже принято. Редактировать можно только если оно ещё не принято"
            })
        else:
            serializer = SpecificationOfPerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'state': 1, 'message': 'Изменено', })
            else:
                return Response({'state': 0, 'message': serializer.errors})
