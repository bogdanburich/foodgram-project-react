from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().me(request, *args, **kwargs)

        return Response(
            {"detail": "User unauthorized."},
            status=status.HTTP_401_UNAUTHORIZED
        )
