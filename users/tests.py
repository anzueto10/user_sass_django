from django.test import TestCase
from django.contrib.auth import authenticate
from users.models import User
class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="Usuario1",
            first_name="Primer",
            last_name="Usuario",
            email="usuario1@gmail.com",
        )
        self.user1.set_password("123user")
        self.user1.save()

        self.user2 = User.objects.create(
            username="Usuario2",
            first_name="Segundo",
            last_name="Usuario",
            email="usuario2@gmail.com",
        )
        self.user2.set_password("123user")
        self.user2.save()

    def test_user_can_login(self):
        user1 = authenticate(username="Usuario1", password="123user")
        self.assertIsNotNone(user1)
        self.assertEqual(user1.username, "Usuario1")

        user2 = authenticate(username="Usuario2", password="123user")
        self.assertIsNotNone(user2)
        self.assertEqual(user2.username, "Usuario2")

        user_wrong = authenticate(username="Usuario1", password="passwordincorrecto")
        self.assertIsNone(user_wrong)
