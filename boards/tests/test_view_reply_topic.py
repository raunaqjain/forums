from django.test import TestCase
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from ..views import reply_topic
from ..forms import PostForm

class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django Test Board')
        self.username = 'raunaq'
        self.password = 'test1234'
        self.user = User.objects.create_user(username=self.username, email='raunaq@cool.com', password=self.password)
        self.topic = Topic.objects.create(subject='Django First Post', board=self.board, starter = self.user)
        Post.objects.create(message='Test Post', topic=self.topic, created_by=self.user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTest(ReplyTopicTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.client.get(self.url), '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/boards/1/topic/1/reply/')
        self.assertEquals(view.func, reply_topic)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)
    
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': "Hello world"})
    
    def test_redirection(self):
        topic_reply_url = reverse('topic_posts', kwargs = {'pk': self.board.pk, 'topic_pk':self.topic.pk})
        self.assertRedirects(self.response, topic_reply_url)
    
    def test_reply_created(self):
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyTopicTest(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': {}})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
