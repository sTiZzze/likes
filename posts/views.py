from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from posts.serializers import UserSerializer, PostSerializer
from posts.models import Post


class PostViewSet(ViewSet):

    def list(self, request):
        """List all issues"""
        post = Post.objects.all() if request.user.is_superuser else Post.objects.filter(user=request.user)
        serializer = PostSerializer(post, many=True)
        return Response({'data': serializer.data})

    def create(self, request):
        """Create a new post"""
        form = PostSerializer(data=request.data)
        form.is_valid(raise_exception=True)
        post = form.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=PostSerializer(post, files=request.FILES).data)
