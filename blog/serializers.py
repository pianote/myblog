from rest_framework import serializers
from .models import Post, Comment

class PostListSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    highlight = serializers.HyperlinkedIdentityField(view_name='blog:post-highlight', format='html')

    class Meta:
        model = Post
        fields = ['author','title','content','date_posted','url','highlight']


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    highlight = serializers.HyperlinkedIdentityField(view_name='blog:post-highlight', format='html')

    class Meta:
        model = Post
        fields = ['author','title','date_posted','url','highlight','content','is_published',
                'photo_main','photo_1','photo_2','photo_3']



class EmptySerializer(serializers.Serializer):
    pass