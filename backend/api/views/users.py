from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import SubscriptionUserSerialzier
from common.constants import ERRORS_KEY
from users.models import Follow

from ..pagination import CustomPageNumberPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().me(request, *args, **kwargs)

        return Response(
            {ERRORS_KEY: "User unauthorized."},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscriptions(request):
    paginator = CustomPageNumberPagination()

    user = request.user
    subscriptions = User.objects.filter(subscriber__subscriber=user)
    result_page = paginator.paginate_queryset(subscriptions, request)
    serializer = SubscriptionUserSerialzier(result_page, many=True,
                                            context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, pk):
    author = get_object_or_404(User, pk=pk)
    user = request.user
    subscription = Follow.objects.filter(author=author, subscriber=user)

    if request.method == 'POST':
        if user == author:
            return Response(
                {ERRORS_KEY: "User cannot be self-subscribed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if subscription.exists():
            return Response(
                {ERRORS_KEY: "Already subscribed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(author=author, subscriber=user)
        serializer = SubscriptionUserSerialzier(author,
                                                context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if not subscription.exists():
        return Response(
            {ERRORS_KEY: "Not subscribed for this user."},
            status=status.HTTP_400_BAD_REQUEST
        )
    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
