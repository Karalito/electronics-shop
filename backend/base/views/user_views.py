from django.contrib.auth.models import update_last_login
from django.core.checks import messages
from django.shortcuts import render
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django.contrib.auth.models import User

from ..serializers import UserSerializer, UserSerializerWithToken

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
import re


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

    if re.search(pattern, data['password']):
        try:
            patternEmail = "[a-zA-Z0-9.]+@[a-zA-Z]+\.(com|net|org)"
            if(re.search(patternEmail, data['email'])):
                user = User.objects.create(
                    first_name=data['name'],
                    last_name=data['surname'],
                    email=data['email'],
                    password=make_password(data['password'])
                )

                serializer = UserSerializerWithToken(user, many=False)
                return Response(serializer.data)
            else:
                message = {
                    'detail': 'Email must contain @ symbol and .com or .net or .org'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except:
            message = {'detail': 'User with this email already exists!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {
            'detail': 'Password must contain: An uppercase and lowercase character, a number and symbol.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    try:
        data = request.data
        user.first_name = data['name']
        user.last_name = data['surname']
        user.email = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()
        return Response(serializer.data)
    except:
        message = {'detail': 'Password cannot be blank!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    
    data = request.data
    user.first_name = data['name']
    user.last_name = data['surname']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):

    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()

    return Response('User was successfully deleted')
