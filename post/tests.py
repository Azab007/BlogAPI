from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Category, Attachment, Image
from django.utils.translation import activate

User = get_user_model()

class PostModelTest(TestCase):
    activate('en')
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create an attachment for testing
        self.attachment = Attachment.objects.create(file='test_attachment.txt')

        # Create an image for testing
        self.image = Image.objects.create(image='test_image.jpg')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    def test_create_post_with_jwt_auth(self):
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content.',
            'author': self.user.pk,
            'categories': [self.category.pk], 
            'attachments': [self.attachment.pk],
            'images': [self.image.pk],
        }

        # Use the JWT token in the Authorization header
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        # Test creating a post with JWT authentication
        response = self.client.post('/api/posts/', data=post_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_post(self):
        post = Post.objects.create(
            title='Initial Title',
            content='Initial content.',
            author=self.user,
        )
        post.categories.add(self.category)
        post.attachments.add(self.attachment)
        post.images.add(self.image)

        # Update the post attributes
        post.title = 'Updated Title'
        post.content = 'Updated content.'
        post.save()

        # Retrieve the updated post from the database
        updated_post = Post.objects.get(pk=post.pk)

        # Check if the updates were applied correctly
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.content, 'Updated content.')

    def test_post_likes_and_dislikes_with_jwt_auth(self):
        # Create a post for testing
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
        )
        
        # Obtain JWT tokens for other users
        user2 = User.objects.create_user(username='user2', password='user2pass')
        user3 = User.objects.create_user(username='user3', password='user3pass')
        refresh2 = RefreshToken.for_user(user2)
        refresh3 = RefreshToken.for_user(user3)
        access_token2 = str(refresh2.access_token)
        access_token3 = str(refresh3.access_token)

        # Use the JWT tokens in the Authorization header
        headers_user2 = {'HTTP_AUTHORIZATION': f'Bearer {access_token2}'}
        headers_user3 = {'HTTP_AUTHORIZATION': f'Bearer {access_token3}'}

        # Test liking a post with JWT authentication
        response_like = self.client.post(f'/api/posts/{post.pk}/like/', **headers_user2)
        self.assertEqual(response_like.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes.count(), 1)

        # Test disliking a post with JWT authentication
        response_dislike = self.client.post(f'/api/posts/{post.pk}/dislike/', **headers_user3)
        self.assertEqual(response_dislike.status_code, status.HTTP_200_OK)
        self.assertEqual(post.dislikes.count(), 1)
    def test_delete_post_with_jwt_auth(self):
        # Create a post for testing
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            author=self.user,
        )

        # Use the JWT token in the Authorization header
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # Test deleting a post with JWT authentication
        response = self.client.delete(f'/api/posts/{post.pk}/', **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to retrieve the deleted post
        with self.assertRaises(Post.DoesNotExist):
            deleted_post = Post.objects.get(pk=post.pk)

    def test_empty_title_with_jwt_auth(self):
        # Attempt to create a post with an empty title
        post_data = {
            'title': '',  # Empty title
            'content': 'This is a test post content.',
            'author': self.user.pk,
        }

        # Use the JWT token in the Authorization header
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # Test creating a post with JWT authentication and an empty title
        response = self.client.post('/api/posts/', data=post_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the expected validation error for the title field
        self.assertIn('title', response.data)
        self.assertIn('This field may not be blank.', response.data['title'])

    def test_create_post_with_missing_content_and_category(self):
        # Attempt to create a post with missing content and category
        post_data = {
            'title': 'Test Post',
            'author': self.user.pk,
        }

        # Use the JWT token in the Authorization header
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        # Test creating a post with JWT authentication and missing fields
        response = self.client.post('/api/posts/', data=post_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains the expected validation errors
        self.assertIn('content', response.data)
        self.assertIn('This field is required.', response.data['content'])
        self.assertIn('categories', response.data)
        self.assertIn('This list may not be empty.', response.data['categories'])

    def test_retrieve_nonexistent_post(self):
        # Attempt to retrieve a post that does not exist
        nonexistent_post_id = 9999

        # Test retrieving a nonexistent post
        response = self.client.get(f'/api/posts/{nonexistent_post_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category_data = {'name': 'Test Category'}
        category = Category.objects.create(**category_data)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, 'Test Category')

class AttachmentModelTest(TestCase):
    def test_create_attachment(self):
        attachment_data = {'file': 'test_attachment.txt'}
        attachment = Attachment.objects.create(**attachment_data)
        self.assertEqual(Attachment.objects.count(), 1)
        self.assertEqual(attachment.file.name, 'test_attachment.txt')

class ImageModelTest(TestCase):
    def test_create_image(self):
        image_data = {'image': 'test_image.jpg'}
        image = Image.objects.create(**image_data)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(image.image.name, 'test_image.jpg')


