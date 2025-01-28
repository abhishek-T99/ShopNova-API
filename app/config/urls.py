# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# from core.views import HealthCheckView

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/user/", include("users.v1.urls", namespace="users")),
#     path("api/health-check/", HealthCheckView.as_view(), name="health-check"),
# ]

# # Media Assets
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Schema URLs
# urlpatterns += [
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#     path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
#     path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
# ]

from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from users.v1.views.user_view import GoogleLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("users.v1.urls", namespace="users")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    path("user/login/google/", GoogleLogin.as_view(), name="google_login"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Schema URLs
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
