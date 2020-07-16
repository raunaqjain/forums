from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
# Create your tests here.


class HomeTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Django', description='Django Test Board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTest(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Django', description='Django Test Board')

    def test_board_topic_view_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topic_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk + 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topic_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topics_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topics_url))


class NewTopicsTest(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name="Django", description="Django Test Board")
        User.objects.create(username='raunaq', email='jraunaq18@gmail.com', password='1234')

    def test_new_topic_view_status_code(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk + 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        data = {
            'subject': 'Test subject',
            'message': 'This is a test message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.post(url, {})
        form = response.context.get("form")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
    
    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)        
