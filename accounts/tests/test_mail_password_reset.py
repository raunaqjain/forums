from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.urls import resolve, reverse

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='raunaq', email='raunaq@cool.com', password='abcd1234')
        self.response = self.client.post(reverse('password_reset'), {'email': 'raunaq@cool.com'})
        self.email = mail.outbox[0]
    
    def test_email_subject(self):
        self.assertEqual('[Django Boards] Please reset your password', self.email.subject)
    
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'token': token,
            'uidb64': uid
        })

        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('raunaq', self.email.body)
        self.assertIn('raunaq@cool.com', self.email.body)
    
    def test_email_to(self):
        self.assertEqual(['raunaq@cool.com',], self.email.to)