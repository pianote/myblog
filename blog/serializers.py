from rest_framework import serializers
from .models import Post, Comment, Reply, Like

class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    
    class Meta:
        model = Like
        fields = ['id','author','post','choice']
    
    
    # def get_or_create(self):
    #     defaults = self.validated_data.copy()
    #     identifier = defaults.pop('unique_field')
    #     return Like.objects.get_or_create(unique_field=identifier, defaults=defaults)


class ReplyListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    # comment = serializers.ReadOnlyField(source='comment.comment_content')
    class Meta:
        model = Reply
        fields = ['author','reply_content']

class CommentListSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedRelatedField(view_name="blog:post-detail", read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="blog:comment-detail")
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['url', 'post', 'reply_count']
    
    def get_reply_count(self, obj):
        count = Reply.objects.filter(comment=obj).count()
        return count


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    post = serializers.HyperlinkedRelatedField(view_name="blog:post-detail", read_only=True)
    replies = ReplyListSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ['post','author','comment_content', 'replies']
    
    def get_replies(self, obj):
        queryset = Reply.objects.filter(comment=obj)
        replies = ReplyListSerializer(queryset, many=True).data
        return replies

class PostListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    comment_count = serializers.SerializerMethodField() #serializers field type is important to use getter method
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['url','comment_count', 'like_count']
    
    def get_comment_count(self, obj):
        count = Comment.objects.filter(post=obj).count()
        return count

    def get_like_count(self, obj):
        count = Like.objects.filter(post=obj, choice=True).count()
        return count

class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    # url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    highlight = serializers.HyperlinkedIdentityField(view_name='blog:post-highlight', format='html')
    # comments = serializers.HyperlinkedRelatedField(many=True, view_name='blog:comment-detail',read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    # comments = CommentDetailSerializer(many=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title','author','content', 'highlight','date_posted','is_published','comments', 'like_count',
                'photo_main','photo_1','photo_2','photo_3']

    def get_comments(self, obj):
        queryset = Comment.objects.filter(post=obj)
        comments = CommentListSerializer(queryset, many=True).data
        return comments
    
    def get_like_count(self, obj):
        count = Like.objects.filter(post=obj, choice=True).count()
        return count
    
    # def get_comments(self, obj):
    #     queryset = Comment.objects.filter(post=obj)
    #     comments_detail = CommentDetailSerializer(queryset, many=True).data
    #     return comments_detail

        
class EmptySerializer(serializers.Serializer):
    pass