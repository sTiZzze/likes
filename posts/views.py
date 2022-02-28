from random import randint

from django.shortcuts import render, redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from posts.serializers import UserSerializer, PostSerializer, PostViewSerializer
from posts.models import Post, View


class PostViewSet(ViewSet):

    def list(self, request):
        """List all issues"""
        post = Post.objects.all() if request.user.is_superuser else Post.objects.filter(user=request.user)
        serializer = PostViewSerializer(post, many=True)
        return Response({'data': serializer.data})

    def create(self, request):
        """Create a new post"""
        form = PostSerializer(data=request.data)
        form.is_valid(raise_exception=True)
        post = form.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=PostSerializer(post, files=request.FILES).data)

    def retrieve(self, request, pk):
        """Query an issue"""
        posts = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, posts)

        serializer = PostViewSerializer(posts)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['GET'])
    def check(self, request, pk):
        count = Post.objects.count()
        post = Post.randoms.all()[randint(0, count - 1)]
        serializer = PostViewSerializer(post, many=False)
        return Response({'data': serializer.data})

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        """Create a new message in an issue"""
        post = get_object_or_404(Post, pk=pk)
        post.like += 1
        post.save()
        return Response(status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        """List all images"""
        post = Post.objects.all() if request.user.is_superuser else Post.objects.filter(user=request.user)
        serializer = PostSerializer(post, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        form = PostSerializer(data=request.data)
        form.is_valid(raise_exception=True)
        post = form.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED, data=PostSerializer(post).data)



