from django.urls import path
from .views import LoginView, TerminateTokenView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("terminate-token/", TerminateTokenView.as_view(), name='terminate-login')
]