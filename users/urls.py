from django.urls import path, include
from rest_framework import routers
from .views import AuthViewSet, password_reset_view

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='auth')

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('password_reset/confirm/<uid>/<token>', password_reset_view, name='pass-reset'),
    # 1. /login
    # 2. /register or /
    # 3. /logout
    # 4. /password_change
    # 5. /refresh
    # 6. /reset_password/
    # 7. /reset_password_confirm/
    # 8. /me/
    # 9. /profile
]
