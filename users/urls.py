from django.urls import path, include
from rest_framework import routers
from .views import AuthViewSet, ProfileAPIView, password_reset_view

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='auth')
# router.register('', UserViewSet, basename='user')

app_name = 'users'

urlpatterns = [

    path('', include(router.urls)),
    path('<pk>/profile', ProfileAPIView.as_view()),
    path('password_reset/confirm/<uid>/<token>', password_reset_view, name='pass-reset'),
    # 1. /login
    # 2. /register
    # 3. /logout
    # 4. /password_change
    # 5. /refresh
    # 6. /profile_update
]
