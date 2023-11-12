from django.test import TestCase
from django import forms
from microblogs.forms import LoginForm

class LogInFormTestCase(TestCase):
    def setUp(self):
        self.valid_input = {'username':'johndoe@gmail.com','passwrod':'Asdf1'}
    

    def test_form_contains_required_fields(self):
        form = LoginForm()
        self.assertIn('username',form.fields)
        self.assertIn('password',form.fields)
        password_field = form.fields['password']
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
        

    