from django.test import TestCase
from microblogs.forms import LoginForm
from django.urls import reverse

class LogInViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('log_in')
        self.valid_input = {
            'username':'john123',
            'first_name':"john",
            'last_name':"doe",
            'email':'john@gmail.com',
            'bio':'ljolijoij',
            'new_password':"Asdf12",
            'password_confirmation':'Asdf12'
        }

    def test_get_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,LoginForm))
        self.assertFalse(form.is_bound)