from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, ReplyViewSet, LikeViewSet
app_name = 'blog'

router = routers.DefaultRouter(trailing_slash=True)
router.register('posts', PostViewSet) 
router.register('comments', CommentViewSet)
router.register('replies', ReplyViewSet)
router.register('likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
