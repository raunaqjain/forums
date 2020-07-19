from django.test import TestCase
from django.urls import reverse, resolve
from ..views import home, board_topics
from ..models import Board
from django.contrib.auth.models import User

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
