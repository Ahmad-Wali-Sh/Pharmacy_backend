from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.user_models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.views import APIView

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='current')
    def current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        permissions = list(user.get_all_permissions())
        additional_permissions = user.additional_permissions.all()
        additional_permissions_list = [str(p) for p in additional_permissions]
        all_permissions = permissions + additional_permissions_list
        return JsonResponse({"permissions": all_permissions})