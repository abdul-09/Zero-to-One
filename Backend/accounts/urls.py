# urls.py
from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, RegisterView, UserDetailView, DashboardView, EnrollTopicView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', UserDetailView.as_view(), name='user_profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('enroll/<int:topic_id>/', EnrollTopicView.as_view(), name='enroll-topic'),
]
