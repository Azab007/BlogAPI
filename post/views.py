from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions, status

from post.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly, IsReaderOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer
import django_filters.rest_framework
from .models import Category
from django.utils.translation import activate

from rest_framework.response import Response
from rest_framework.decorators import action 
class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username')
    publication_date__gte = django_filters.DateTimeFilter(field_name='publication_date', lookup_expr='gte')
    publication_date__lte = django_filters.DateTimeFilter(field_name='publication_date', lookup_expr='lte')
    categories = django_filters.CharFilter(field_name='categories__name')
    tags = django_filters.CharFilter(field_name='tags__name')

    class Meta:
        model = Post
        fields = ['author', 'publication_date__gte', 'publication_date__lte', 'categories', 'tags']


class CommentViewSet(viewsets.ModelViewSet):
    activate('ar')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post, author=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    activate('ar')
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsReaderOrReadOnly]
        elif self.action in ["like",'dislike']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
        else:
            permission_classes = [IsAdminOrReadOnly]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            post.dislikes.remove(user)

        post.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.dislikes.all():
            post.dislikes.remove(user)
        else:
            post.dislikes.add(user)
            post.likes.remove(user)

        post.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
