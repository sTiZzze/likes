from random import randint
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models import Count, Q

from posts.serializers import UserSerializer, PostSerializer, PostViewSerializer
from posts.models import Post
from posts.tasks import like_post
from posts.permissions import PostPermission


class PostViewSet(ViewSet):

    permission_classes = (PostPermission,)

    def list(self, request):
        """List all issues"""
        post = Post.objects.all() if request.user.is_superuser else Post.objects.filter(user=request.user)
        serializer = PostViewSerializer(post, many=True)
        return Response({'data': serializer.data})

    def retrieve(self, request, pk):
        """Query an issue"""
        posts = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, posts)
        serializer = PostViewSerializer(posts)
        return Response({'data': serializer.data})

    @action(detail=False, methods=['get'])
    def check(self, request):
        count = Post.objects.filter(is_blocked=False).count()
        try:
            post = Post.randoms.all().filter(is_blocked=False).exclude(view=self.request.user)[randint(0, count - 1)]
            serializer = PostViewSerializer(post, many=False)
            post.view.add(request.user)
            post.save()
            return Response({'data': serializer.data})
        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Directory is empty')

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        """Create a new message in an issue"""
        post = get_object_or_404(Post, pk=pk)
        #post.like.add(request.user.id)
        #post.save()
        task = like_post.delay(post.id, request.user.id)
        task.wait()
        total_like = post.total_like
        return Response(status=status.HTTP_200_OK, data=total_like)

    @action(detail=True, methods=['post'])
    def report(self, request, pk):
        """Create a new message in an issue"""
        post = get_object_or_404(Post, pk=pk)
        post.report.add(request.user)
        post.block_post()
        post.save()
        total_report = post.total_report
        return Response(status=status.HTTP_200_OK, data=total_report)

    @action(detail=False, methods=['get'])
    def top(self, request):
        post = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')[:5]
        serializer = PostViewSerializer(post, many=True)
        return Response({'data': serializer.data})


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)

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



