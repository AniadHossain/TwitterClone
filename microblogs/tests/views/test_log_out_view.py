from django.test import TestCase
from django.urls import reverse
from microblogs.models import User
from microblogs.tests.helpers import LogInTester

class LogOutViewTestCase(TestCase,LogInTester):

    fixtures = ['microblogs/tests/fixtures/default_user.json']
    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(username = "Aniad123")

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        pass
        self.client.login(username = 'Aniad123', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url,follow = True)
        response_url = reverse('home')
        self.assertRedirects(response,response_url,status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'home.html')
        self.assertFalse(self._is_logged_in())