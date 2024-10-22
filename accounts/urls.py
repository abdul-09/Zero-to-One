# urls.py
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    EnrollTrainingView, GoogleLoginCallback, LoginView,  LogoutView, PasswordResetView, PasswordResetConfirmView, RegisterView, ProfileUpdateView, DashboardView, GoogleLoginView, ResourcesView, TopicView, TrainingScheduleView
)

# path('auth/login/', TokenObtainPairView.as_view(), name='jwt-login'), LoginView,
    
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls")),
    # path("login/", LoginPage.as_view(), name="login"),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLoginView.as_view(), name="google_login"),
    path(
        "api/v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    # path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('topic/', TopicView.as_view(), name='interestedtopics'),
    path('resource/', ResourcesView.as_view(), name='resources'),
    path('trainings/', TrainingScheduleView.as_view(), name='schedule'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('enroll/<int:training_id>/', EnrollTrainingView.as_view(), name='enroll-training'),
    # path('captcha/', include('captcha.urls')),

]


urlpatterns += staticfiles_urlpatterns()