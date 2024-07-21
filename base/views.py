# views.py
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer, VerifyAccountSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from .validators import validate_password
from .models import User
from .emails import send_otp_for_verification_email
from rest_framework.views import APIView


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
            send_otp_for_verification_email(serializer.data['email'])
            return Response({'message': 'Registration Successful. Please Check your email for Email Validation OTP'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # If password validation fails, return the errors
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                otp = serializer.validated_data.get('otp')
                
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'User not found',
                        'data': 'Invalid email address provided.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Invalid OTP',
                        'data': 'The OTP you entered is incorrect.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = user.first()
                user.is_email_verified = True
                user.save()
                
                return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'data': {}
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'Invalid data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError as ke:
            return Response({
                'status': 500,
                'message': 'Missing key in serializer data',
                'data': str(ke)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)