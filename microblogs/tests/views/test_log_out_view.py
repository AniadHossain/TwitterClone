from django.test import TestCase
from django.urls import reverse
from microblogs.models import User
from microblogs.tests.helpers import LogInTester

class LogOutViewTestCase(TestCase,LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user(
            "AniadHossain",
            first_name='Aniad',
            last_name="Hossain",
            email="aniad.hossain@outlook.com",
            password="Password123",
            bio="Chilling"
        )

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        pass
        self.client.login(username = 'AniadHossain', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url,follow = True)
        response_url = reverse('home')
        self.assertRedirects(response,response_url,status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'home.html')
        self.assertFalse(self._is_logged_in())