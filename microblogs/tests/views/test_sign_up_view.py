from django.test import TestCase
from microblogs.forms import SignUpForm
from microblogs.models import User
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from microblogs.tests.helpers import LogInTester

class SignUpViewTestCase(TestCase,LogInTester):

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')
        self.valid_input = {
            'username':'john123',
            'first_name':"john",
            'last_name':"doe",
            'email':'john@gmail.com',
            'bio':'ljolijoij',
            'new_password':"Asdf12",
            'password_confirmation':'Asdf12'
        }

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,SignUpForm))
        self.assertFalse(form.is_bound)

    def test_get_sign_up_when_logged_in(self):
        self.client.login(username='Aniad123',password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response,reverse('feed'),status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')

    def test_unsuccessful_sign_up(self):
        self.valid_input['new_password'] = 'jjjjj'
        response = self.client.post(self.url,self.valid_input)
        self.assertTemplateUsed(response,'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form,SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())


    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url,self.valid_input,follow=True)
        after_count = User.objects.count()
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')
        self.assertEqual(after_count,before_count + 1)
        user = User.objects.get(username = "john123")
        self.assertEqual(user.first_name,"john")
        self.assertEqual(user.last_name,"doe")
        self.assertEqual(user.email,"john@gmail.com")
        self.assertEqual(user.bio,"ljolijoij")
        self.assertTrue(check_password("Asdf12",user.password))
        self.assertTrue(self._is_logged_in())

    def test_post_sign_up_when_logged_in(self):
        before_count = User.objects.count()
        self.client.login(username='Aniad123',password='Password123')
        response = self.client.post(self.url, self.valid_input ,follow=True)
        after_count = User.objects.count()
        self.assertRedirects(response,reverse('feed'),status_code=302,target_status_code=200)
        self.assertTemplateUsed(response,'feed.html')
        self.assertEqual(before_count,after_count)



