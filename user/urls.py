from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPermissionsView
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls + [
    path("users/current/permissions/", UserPermissionsView.as_view(), name="user-permissions")
]