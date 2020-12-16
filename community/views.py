from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CommunityListSerializer, CommunitySerializer, CommentSerializer
from .models import Community, Comment


@api_view(['GET', 'POST'])
def community_list_create(request):
    if request.method == 'GET':
        communities = Community.objects.all()
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)
    else:
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def community_detail_update_delete(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    if request.method == 'GET':
        serializer = CommunitySerializer(community)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        community.delete()
        return Response({ 'id': community_pk }, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_comment(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(community=community)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail_update_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        comment.delete()
        return Response({ 'id': comment_pk }, status=status.HTTP_204_NO_CONTENT)
