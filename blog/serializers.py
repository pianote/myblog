from rest_framework import serializers
from .models import Post, Comment

class PostListSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    highlight = serializers.HyperlinkedIdentityField(view_name='blog:post-highlight', format='html')
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='blog:comment-detail',read_only=True)

    class Meta:
        model = Post
        fields = ['author','title','content','date_posted','url','highlight','comments']

class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    highlight = serializers.HyperlinkedIdentityField(view_name='blog:post-highlight', format='html')
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='blog:comment-detail',read_only=True)

    class Meta:
        model = Post
        fields = ['author','title','date_posted','url','highlight','content','is_published','comments',
                'photo_main','photo_1','photo_2','photo_3']

class CommentSerializer(serializers.ModelSerializer):
    # comment_author = serializers.ReadOnlyField(source='comment_author.name')
    # post = serializers.ReadOnlyField(source='post.title')
    # url = serializers.HyperlinkedIdentityField(view_name="blog:comment-detail")
    class Meta:
        model = Comment
        fields = ['post','comment_author','comment_content']

class EmptySerializer(serializers.Serializer):
    pass