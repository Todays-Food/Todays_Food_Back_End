from rest_framework import serializers
from .models import Community, Comment


class CommunityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'title',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'community',)
        read_only_fields = ('community',)


class CommunitySerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(
        many=True,
        read_only=True,
    )
    comment_count = serializers.IntegerField(
        source='comment_set.count',
        read_only=True,
    )
    class Meta:
        model = Community
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'comment_set', 'comment_count',)