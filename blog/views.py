from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status, renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from . import serializers

class PostViewSet(viewsets.ModelViewSet):
    """
    This "ModelViewSet" viewset automatically provides `list` and `detail` actions.
    write permission for onwer
    readonly permission the rest
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all().order_by('-created_date')
   
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PostDetailSerializer
        return serializers.PostListSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.content)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
