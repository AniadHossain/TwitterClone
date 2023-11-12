from django.test import TestCase
from microblogs.forms import SignUpForm
from microblogs.models import User
from django.contrib.auth.hashers import check_password
from django.urls import reverse

class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.valid_input = {
            'username':'john123',
            'first_name':"john",
            'last_name':"doe",
            'email':'john@gmail.com',
            'bio':'ljolijoij',
            'new_password':"Asdf12",
            'password_confirmation':'Asdf12'
        }


    #Form has the neccessary fields
    

    #Form accpects valid input data
    def test_valid_sign_up_form(self):
        form = SignUpForm(data = self.valid_input)
        self.assertTrue(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data = self.valid_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count,before_count + 1)
        user = User.objects.get(username = "john123")
        self.assertEqual(user.first_name,"john")
        self.assertEqual(user.last_name,"doe")
        self.assertEqual(user.email,"john@gmail.com")
        self.assertEqual(user.bio,"ljolijoij")
        self.assertTrue(check_password("Asdf12",user.password))
