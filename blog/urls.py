from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet
app_name = 'blog'

router = routers.DefaultRouter(trailing_slash=True)
router.register('posts', PostViewSet) #post-detail, post-list ...

urlpatterns = [
    path('', include(router.urls)),
]