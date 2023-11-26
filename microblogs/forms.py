from django import forms
from .models import User, Post
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','bio']
        widgets = {'bio':forms.Textarea()}

    new_password = forms.CharField(label = "Password", 
                                   widget=forms.PasswordInput(),
                                   validators=[RegexValidator(
                                       regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                                       message='Passwowrd must contain an uppercase letter and a lower case letter and a number'
                                   )])
    password_confirmation = forms.CharField(label = "Password Confirmation", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if(password_confirmation != new_password):
            self.add_error("password_confirmation",'Confirmaiton does not match password.')

    def save(self):
        super().save(commit=False)
        
        return User.objects.create_user(
                self.cleaned_data.get('username'),
                first_name = self.cleaned_data.get('first_name'),
                last_name = self.cleaned_data.get('last_name'),
                email = self.cleaned_data.get('email'),
                bio = self.cleaned_data.get('bio'),
                password = self.cleaned_data.get('new_password')
            )
    
class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password",widget=forms.PasswordInput)

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets = { 'bio': forms.Textarea() }

class PasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

class PostForm(forms.ModelForm):
    """Form to ask user for post text.

    The post author must be by the post creator.
    """

    class Meta:
        """Form options."""

        model = Post
        fields = ['text']
        widgets = {
            'text': forms.Textarea()
        }
