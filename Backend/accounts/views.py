# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import generics

from .models import User, InterestedTopic
from .serializers import RegisterSerializer, UserSerializer, UserDashboardSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)


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

        reset_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"
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

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if not new_password or len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

class DashboardView(generics.RetrieveAPIView):
    """
    Retrieve the dashboard data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserDashboardSerializer

    def get_object(self):
        return self.request.user

class EnrollTopicView(APIView):
    """
    Enroll the authenticated user in a specified topic.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, topic_id):
        user = request.user
        try:
            topic = InterestedTopic.objects.get(id=topic_id)
        except InterestedTopic.DoesNotExist:
            return Response({"error": "Topic does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already enrolled
        if user.interested_topics.filter(id=topic_id).exists():
            return Response({"message": "Already enrolled in this topic."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Enroll the user
        user.interested_topics.add(topic)
        return Response({"message": "Successfully enrolled in the topic."}, status=status.HTTP_200_OK)