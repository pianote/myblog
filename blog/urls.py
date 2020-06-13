from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet
app_name = 'blog'

router = routers.DefaultRouter(trailing_slash=True)
router.register('posts', PostViewSet) #post-detail, post-list ...
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]