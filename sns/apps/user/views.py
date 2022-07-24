from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserInfoScheme, UserSignInSerializer, UserSignUpSerializer, UserUpdateSerializer


# Create your views here.
class UserSignUpView(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignUpSerializer)
    def post(self, reqeust):
        serializer = UserSignUpSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "success, user sign-up"}, status=status.HTTP_201_CREATED)


class UserUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    @api_view(['PATCH'])
    @swagger_auto_schema(request_body=UserUpdateSerializer)
    def user_update(request):
        user = User.objects.filter(id=request.user.id).first()

        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "success, user update"}, status=status.HTTP_202_ACCEPTED)


class UserSignInView(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignInSerializer, responses={200: UserInfoScheme})
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.user_signin(data=request.data), status=status.HTTP_200_OK)


class UserSignOutView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserSignInSerializer)
    def post(self, request):
        Refresh_token = request.data["refresh"]
        token = RefreshToken(Refresh_token)
        token.blacklist()

        return Response({"detail": "success, signout"}, status=status.HTTP_200_OK)
