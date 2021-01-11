from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import CommunityListSerializer,  CommentSerializer
from .models import Community, Comment
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def community_list_create(request):
    if request.method == 'GET':
        communities = Community.objects.all()
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)
    else:
        serializer = CommunityListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def community_detail_update_delete(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    print('@@@유저 출력:', request.user)
    if request.method == 'GET':
        serializer = CommunityListSerializer(community)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CommunityListSerializer(community, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        community.delete()
        return Response({ 'id': community_pk }, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated]) 
def like(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    # print('@@@@@@@', request.user.id)
    serializer = CommunityListSerializer(community, data=request.data)
    print('시리얼라이저: ', request.data)
    user = request.data['user_id']
    # print('시리얼라이저: ', request.data['user'])
    print('좋아요', community.like_users.all())
    if request.method == "POST":
        # user = request.data['user_id']
        like = False
        community = get_object_or_404(Community, pk=community_pk)
        if user in community.like_users.all():
            community.like_users.remove(user)
        else:
            community.like_users.add(user)
            like = True
        return Response({'msg': like})
    else:
        like = False
        community = get_object_or_404(Community, pk=community_pk)
        # user = request.data
        print('USER: ', request.data)
        if user in community.like_users.all():
            like = True
        else:
            like = False
        return Response({'msg': like})


# @api_view(['POST'])
# def create_comment(request, community_pk):
#     community = get_object_or_404(Community, pk=community_pk)
#     comment = Comment(content=request.data.get('content'), community=community, user=request.user)
#     comment.save()
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(community=community)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# def comment_list(request):
#     comments = Comment.objects.filter(pk=community_pk)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def comment_detail_update_delete(request, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     else:
#         comment.delete()
#         return Response({ 'id': comment_pk }, status=status.HTTP_204_NO_CONTENT)

