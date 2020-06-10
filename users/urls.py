from django.urls import path, include
from rest_framework import routers
from .views import AuthViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='auth')

urlpatterns = [

    path('', include(router.urls)),
    # path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # 1. /login
    # 2. /register
    # 3. /logout
    # 4. /password_change
]