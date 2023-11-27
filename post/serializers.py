from rest_framework import serializers
from .models import Category, Attachment, Image, Post, Comment
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
        ref_name='PostUserSerializer'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id', read_only=True)
    post = serializers.ReadOnlyField(source='post.id', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True,required=False)
    images = ImageSerializer(many=True,required=False)
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id', read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        images_data = validated_data.pop('images', [])
        categories_data = validated_data.pop('categories', [])
        likes_data = validated_data.pop('likes', [])
        dislikes_data = validated_data.pop('dislikes', [])


        post = Post.objects.create(**validated_data)
        for category_data in categories_data:
            post.categories.add(category_data)

        for like_data in likes_data:
            post.likes.add(like_data)

        for dislike_data in dislikes_data:
            post.categories.add(dislike_data)
        
        for attachment_data in attachments_data:
            if dict(attachment_data) != {}:
                attachment = Attachment.objects.create(**attachment_data)
                post.attachments.add(attachment)
        for image_data in images_data:
            if dict(image_data) != {}:
                image = Image.objects.create(**image_data)
                post.images.add(image)
        return post
    
class PostIdSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()