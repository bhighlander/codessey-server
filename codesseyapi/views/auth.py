"""Programmer model"""

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from codesseyapi.models import Programmer

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Handles the creation of a new user for authentication
    
    Method arguments:
        request -- The full HTTP request object
    """

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
    data = { 'token': token.key }
    return Response(data)
