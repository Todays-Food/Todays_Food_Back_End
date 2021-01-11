from rest_framework import serializers
from .models import Community, Comment

# 게시글 리스트
class CommunityListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Community
        # fields = ('id', 'title', 'content', 'created_at', 'updated_at',)
        # fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user',)
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user', 'like_users', 'user_id',)
        # fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user', 'user_id',)


# 댓글
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        # fields = ('id', 'content', 'community',)
        fields = ('id', 'content', 'community', 'user',)
        # fields = ('id', 'content', 'community', 'user', 'like_users',)
        # read_only_fields = ('community',)


# 게시글 하나
# class CommunitySerializer(serializers.ModelSerializer):
#     comment_set = CommentSerializer(
#         many=True,
#         read_only=True,
#     )
#     comment_count = serializers.IntegerField(
#         source='comment_set.count',
#         read_only=True,
#     )
#     class Meta:
#         model = Community
#         fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'comment_set', 'comment_count',)
        # fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'comment_set', 'comment_count', 'user',)