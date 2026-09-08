from django.shortcuts import render
from django.conf import settings
from  f_auth.models import User, UserProfile
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleLoginView(APIView):

    def post(self, request):

        google_token = request.data.get("token")

        if not google_token:
            return Response(
                {"message": "Google token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # Verify Google ID token
            google_user = id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            google_id = google_user["sub"]

            email = google_user.get("email")
            name = google_user.get("name", "")
            picture = google_user.get("picture")

            user = User.objects.filter(
                email=email
            ).first()

            if not user:

                user = User.objects.create(
                    email=email,
                )
                userprofile = UserProfile.objects.create(
                    user=user,
                    first_name=name.split(" ")[0] if name else "",
                    last_name=" ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else "",
                    profile_picture_url=picture
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Google login successful",

                "access": str(refresh.access_token),

                "refresh": str(refresh),

                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                }
            })

        except ValueError:

            return Response(
                {"message": "Invalid Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )