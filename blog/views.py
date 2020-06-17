from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment, Reply, Like
from . import serializers

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all().order_by('-created_date')
   
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        return serializers.PostDetailSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.content)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comment.objects.all().order_by('-created_date')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentListSerializer
        return serializers.CommentDetailSerializer

class ReplyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Reply.objects.all().order_by('-created_date')
    serializer_class = serializers.ReplyListSerializer

from rest_framework import mixins

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Like.objects.all().order_by('-created_date')
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        post = validated_data.get('post')
        instance, created = Like.objects.get_or_create(post=post, author=self.request.user)
        #Check if a like for this post exist
        #create a like instance if not exist -> created == True
        if not created: #like already exist
            #update like instance with new data ('choice',)
            serializer.update(instance, validated_data)
        else:
            serializer.save(author=self.request.user)



