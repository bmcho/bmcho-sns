import re

from django.contrib.auth.hashers import check_password
from rest_framework import exceptions, serializers
from rest_framework.views import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """유저 가입 serializer

    Writer: 조병민
    Date: 2022-07-21

    """

    def create(self, validated_data):
        password = validated_data.get('password')

        # 패스워드 정규식표현(최소 1개 이상의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성/ 길이는 8~20자리)
        password_regexp = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}$'

        if not re.match(password_regexp, password):
            raise_exception = exceptions.APIException(detail="inaccurate password")
            raise_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise raise_exception

        # 유저정보 DB 저장
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['email', 'nickname', 'introduce', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):
    """유저 수정 serializer

    Writer: 조병민
    Date: 2022-07-21

    """

    def update(self, instance, validated_data):

        if not instance or not check_password(validated_data['password'], instance.password):
            raise_exception = exceptions.APIException(detail="inaccurate user info")
            raise_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise raise_exception

        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.introduce = validated_data.get('introduce', instance.introduce)
        instance.save(raise_exception=True)
        return instance

    class Meta:
        model = User
        fields = ['nickname', 'introduce', 'password']


class UserInfoScheme(serializers.Serializer):
    """유저 로그인 scheme

    Writer: 조병민
    Date: 2022-07-21

    """

    user_info = serializers.CharField()
    refresh = serializers.CharField()
    access = serializers.CharField()


class UserSignInSerializer(TokenObtainPairSerializer):
    """로그인 Serializer

    Writer: 조병민
    Date: 2022-07-21

    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=255)

    def user_signin(self, data):
        user = User.objects.get(email=data['email'])
        if not user or not check_password(data['password'], user.password):
            raise_exception = exceptions.APIException(detail="inaccurate user info")
            raise_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise raise_exception

        refresh = super().get_token(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        data = {'user_info': str(user), 'refresh': refresh_token, 'access': access_token}
        serializer = UserInfoScheme(data=data)
        serializer.is_valid(raise_exception=True)

        return serializer.data
