from django.test import TestCase
from microblogs.forms import LoginForm
from django.urls import reverse
from microblogs.models import User
from microblogs.tests.helpers import LogInTester

class LogInViewTestCase(TestCase,LogInTester):

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username = "Aniad123")

    def test_get_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,LoginForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = {'username':'johndoe','password':'WrongPassword123'}
        response = self.client.post(self.url,form_input)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,LoginForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {'username':'Aniad123','password':'Password123'}
        response = self.client.post(self.url,form_input,follow=True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')
        self.assertTrue(self._is_logged_in())

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'username':'Aniad123','password':'Password123'}
        response = self.client.post(self.url,form_input,follow=True)

        self.assertTemplateUsed(response,'log_in.html')
        self.assertFalse(self._is_logged_in())
    
    