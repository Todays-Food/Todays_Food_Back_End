from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED
) 
from .serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    print('여기는 들어왔나?')
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    print(password)
    print(password_confirmation)
    if password != password_confirmation:
        print('일치하지 않습니다!!')
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data) 
    if serializer.is_valid(raise_exception=True):
        print('여기로 왔나??')
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=HTTP_201_CREATED)   