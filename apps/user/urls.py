from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Put here views here
urlpatterns = [
]

internal_urls = [
    path('token/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
]

urlpatterns += internal_urls
