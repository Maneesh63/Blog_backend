from django.urls import path
from .views import GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleLoginView.as_view(), name="google-login"),
] 