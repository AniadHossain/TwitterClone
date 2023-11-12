from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User

# Create your tests here.

class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            "AniadHossain",
            first_name='Aniad',
            last_name="Hossain",
            email="aniad.hossain@outlook.com",
            password="password123",
            bio="Chilling"
        )

    def test_valid_user(self):
        self._assert_user_is_valid()


    def test_email_cannot_be_empty(self):

        self.user.email = ""

        self._assert_user_is_invalid()

    def test_username_can_be_20_characters_long(self):
        self.user.username = '@' + 'x' * 19
        self._assert_user_is_valid()


    def test_username_can_be_over_20_characters_long(self):
        self.user.username = '@' + 'x' * 20
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        User.objects.create_user(
            "boob",
            first_name='bob',
            last_name="marley",
            email="bob@outlook.com",
            password="password1234",
            bio="bored"
        )

        self.user.username="boob"
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        User.objects.create_user(
            username="uniqueuser",
            first_name='John',
            last_name="Doe",
            email="unique@example.com",
            password="password1234",
            bio="Testing"
        )

        self.user.email = "unique@example.com"
        self._assert_user_is_invalid()

    def test_bio_max_length_exceeded(self):
        self.user.bio = 'A' * 521  # Exceeds the max_length of 520
        self._assert_user_is_invalid()

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

        def test_username_cannot_be_empty(self):
            self.user.username = ""
            self._assert_user_is_invalid()

        def test_first_name_cannot_be_empty(self):
            self.user.first_name = ""
            self._assert_user_is_invalid()

        def test_last_name_cannot_be_empty(self):
            self.user.last_name = ""
            self._assert_user_is_invalid()

        def test_password_cannot_be_empty(self):
            self.user.password = ""
            self._assert_user_is_invalid()

        def test_email_must_contain_at_symbol(self):
            self.user.email = "aniad.hossain.outlook.com"
            self._assert_user_is_invalid()

        def test_email_must_contain_period(self):
            self.user.email = "aniad@hossain@outlook@com"
            self._assert_user_is_invalid()

        def test_email_cannot_be_over_254_characters_long(self):
            self.user.email = "a" * 247 + "@example.com"
            self._assert_user_is_valid()

            self.user.email += "a"
            self._assert_user_is_invalid()

        def test_username_cannot_contain_spaces(self):
            self.user.username = "aniad hossain"
            self._assert_user_is_invalid()

        def test_username_cannot_contain_special_characters(self):
            self.user.username = "aniad$hossain"
            self._assert_user_is_invalid()

        def test_bio_can_be_empty(self):
            self.user.bio = ""
            self._assert_user_is_valid()
            
        def test_bio_max_length(self):
            self.user.bio = 'A' * 520
            self._assert_user_is_valid()


