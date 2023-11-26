from rest_framework import serializers
from .models import Category, Post, Comment



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id', read_only=True)
    post = serializers.ReadOnlyField(source='post.id',read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
