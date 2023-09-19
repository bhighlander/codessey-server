"""Programmer model"""

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth import authenticate
from codesseyapi.models import Programmer
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Handles the creation of a new user for authentication
    
    Method arguments:
        request -- The full HTTP request object
    """
    try:
        new_user = User.objects.create_user(
            first_name = request.data['first_name'],
            last_name = request.data['last_name'],
            email = request.data['email'],
            username = request.data['username'],
            password = request.data['password'],
        )

        programmer = Programmer.objects.create(
            user=new_user,
        )
        token = Token.objects.create(user=programmer.user)
        data = { 'token': token.key, 'valid': True }
        return Response(data)
    except IntegrityError:
        data = { 'valid': False, 'error': 'Username already exists. Please choose a different one.' }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Handles the authentication of a user
    
    Method arguments:
        request -- The full HTTP request object
    """

    username = request.data['username']
    password = request.data['password']
    print(request.data)
    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        programmer = Programmer.objects.get(user=authenticated_user)
        token = Token.objects.get(user=programmer.user)
        data = { 'valid': True, 'token': token.key }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)