from django.test import TestCase
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from ..views import PostListView

class TopicPostsTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django Test Board')
        user = User.objects.create_user(username='raunaq', email='raunaq@cool.com', password='test1234')
        topic = Topic.objects.create(subject='Django First Post', board=board, starter = user)
        Post.objects.create(message='Test Post', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        return self.assertEquals(self.response.status_code, 200)
    
    def test_view_func(self):
        view = resolve('/boards/1/topic/1/')
        return self.assertEquals(view.func.view_class, PostListView)