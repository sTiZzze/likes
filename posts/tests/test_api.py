from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post


class PostsApiUserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.client.login(username='testuser', password='12345')

    def test_create_post(self):
        url = reverse('posts-list')
        data = {'image'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.get()

        self.assertEqual(post.image, 'image')
