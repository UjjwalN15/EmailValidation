# views.py
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from .validators import validate_password
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        phone = request.data.get('phone')
        if User.objects.filter(phone=phone).exists():
            return Response({'phone': ['Phone number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate the password
            validate_password(password)
            # Save the user instance
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # If password validation fails, return the errors
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
