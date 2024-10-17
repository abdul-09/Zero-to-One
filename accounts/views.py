# views.py
from django.shortcuts import render
from django.views import View
import requests
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail
from urllib.parse import urljoin
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import generics

from .models import TrainingSchedule, User, InterestedTopic
from .serializers import ProfileUpdateSerializer, RegisterSerializer, UserDashboardSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class GoogleLoginView(SocialLoginView):
    permission_classes = [AllowAny]

    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        This endpoint will handle the OAuth2 code exchange and return the JWT tokens.
        Ensure the 'code' from Google is exchanged for access and refresh tokens.
        """

        code = request.GET.get("code")

        if not code:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for tokens
       
        # Instantiate the OAuth2 client and exchange the code

        token_endpoint_url = 'https://oauth2.googleapis.com/token'
        data = {
                'code': code,
                'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
                'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
                'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
                'grant_type': 'authorization_code',
            }

            # Make a request to the token endpoint
        response = requests.post(token_endpoint_url, data=data)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch token."}, status=response.status_code)
            
        tokens = response.json()
        id_token_google = tokens.get('id_token')

        try:
                # Step 2: Verify Google ID Token
                idinfo = id_token.verify_oauth2_token(id_token_google, google_requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)

                # Get the user’s email from the token (or any other information you need)
                email = idinfo.get('email')

                # Step 3: Generate your own JWT token (or login the user)
                # This assumes you're using Django Simple JWT or similar
                user, _ = User.objects.get_or_create(email=email)  # Replace with your user model logic

                # Generate JWT for your application
                refresh = RefreshToken.for_user(user)
                jwt_tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                # Return your app's JWT tokens
                return Response(jwt_tokens, status=status.HTTP_200_OK)

        except ValueError:
            # Invalid token
            return Response({"error": "Invalid ID token"}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Log the user
            logout(request)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"https://frontdeploy-zero2one.vercel.app/auth/password/reset-password-confirmation/?uid={uid}&token={token}/"
        send_mail(
            'Password Reset',
            f'Click the link to reset your password: {reset_link}',
            'no-reply@yourdomain.com',
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')

        print("Received UID:", uid)
        print("Received Token:", token)
        print("New Password:", new_password)
        print("Re-New Password:", re_new_password)

        if not all([uid, token, new_password, re_new_password]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            u_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=u_id)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

# class PasswordResetConfirmView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request, uidb64, token):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

#         token_generator = PasswordResetTokenGenerator()
#         if not token_generator.check_token(user, token):
#             return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate the password
#         new_password = request.data.get('password')
#         if not new_password or len(new_password) < 8:
#             return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Set the new password and save the user
#         user.set_password(new_password)
#         user.save()

#         return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

class DashboardView(generics.RetrieveAPIView):
    """
    Retrieve the dashboard data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserDashboardSerializer

    def get_object(self):
        return self.request.user

class EnrollTrainingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, training_id):
        user = request.user
        try:
            training = TrainingSchedule.objects.get(id=training_id)
        except TrainingSchedule.DoesNotExist:
            return Response({"error": "Training does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if already enrolled
        if user.enrolled_trainings.filter(id=training_id).exists():
            return Response({"message": "Already enrolled in this training."}, status=status.HTTP_400_BAD_REQUEST)

        # Enroll the user
        user.enrolled_trainings.add(training)
        return Response({"message": "Successfully enrolled in the training."}, status=status.HTTP_200_OK)