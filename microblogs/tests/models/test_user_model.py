from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User

# Create your tests here.

class UserModelTestCase(TestCase):

    fixtures = ['microblogs/tests/fixtures/default_user.json','microblogs/tests/fixtures/other_users.json']
    def setUp(self):
        self.user = User.objects.get(username="Aniad123")

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
        self._assert_user_is_invalid()

        self.user.email += "a"
        self._assert_user_is_invalid()

    def test_bio_can_be_empty(self):
        self.user.bio = ""
        self._assert_user_is_valid()
        
    def test_bio_max_length(self):
        self.user.bio = 'A' * 520
        self._assert_user_is_valid()

    def test_toggle_follow(self):
        jane = User.objects.get(username="Jane123")
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertTrue(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))

    def test_follow_counters(self):
        jane = User.objects.get(username="Jane123")
        petra = User.objects.get(username="Petra123")
        peter = User.objects.get(username="Peter123")

        # Check initial follow counts
        self.assertEqual(jane.follower_count(), 0)
        self.assertEqual(jane.followee_count(), 0)
        self.assertEqual(petra.follower_count(), 0)
        self.assertEqual(petra.followee_count(), 0)
        self.assertEqual(peter.follower_count(), 0)
        self.assertEqual(peter.followee_count(), 0)

        # Have jane follow petra and peter
        jane.toggle_follow(petra)
        jane.toggle_follow(peter)

        # Check follow counts after jane follows petra and peter
        self.assertEqual(jane.follower_count(), 0)
        self.assertEqual(jane.followee_count(), 2)
        self.assertEqual(petra.follower_count(), 1)
        self.assertEqual(petra.followee_count(), 0)
        self.assertEqual(peter.follower_count(), 1)
        self.assertEqual(peter.followee_count(), 0)

        # Have petra follow jane
        petra.toggle_follow(jane)

        # Check follow counts after petra follows jane
        self.assertEqual(jane.follower_count(), 1)
        self.assertEqual(jane.followee_count(), 2)
        self.assertEqual(petra.follower_count(), 1)
        self.assertEqual(petra.followee_count(), 1)
        self.assertEqual(peter.follower_count(), 1)
        self.assertEqual(peter.followee_count(), 0)

        # Have peter follow jane
        peter.toggle_follow(jane)

        # Check follow counts after peter follows jane
        self.assertEqual(jane.follower_count(), 2)
        self.assertEqual(jane.followee_count(), 2)
        self.assertEqual(petra.follower_count(), 1)
        self.assertEqual(petra.followee_count(), 1)
        self.assertEqual(peter.follower_count(), 1)
        self.assertEqual(peter.followee_count(), 1)

            
            



