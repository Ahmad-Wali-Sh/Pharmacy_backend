from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate



class TerminateTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
                token.delete() 
                return Response({'detail': 'Token successfully deleted.'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'detail': 'No active token found for this user.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'detail': 'Logout successfully deleted.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'detail': 'No active token found for this user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                token = Token.objects.get(user=user)
                token.delete()
            except Token.DoesNotExist:
                pass

            new_token, created = Token.objects.get_or_create(user=user)

            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
