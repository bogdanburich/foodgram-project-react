from django.shortcuts import get_object_or_404
from recipes.models import Tag
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TagSerializer


class TagViewSet(viewsets.ViewSet):

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
