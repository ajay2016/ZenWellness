from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Discipline
from ..constants import STAFF, ACTIVE


class TestCustomUserModel(TestCase):

    PHONE_NUMBER = '9812323232'
    PASSWORD = 'random@pass'

    def test_can_create_user_with_phonenumber_and_password(self):
        user = get_user_model().objects.create_user(
            phone_number=self.PHONE_NUMBER,
            password=self.PASSWORD
        )
        self.assertEqual(user.phone_number, self.PHONE_NUMBER)
        self.assertTrue(user.check_password(self.PASSWORD))

    def test_cannot_create_user_without_phone_and_password(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                phone_number='',
                password='',
                user_type=''
            )

    def test_can_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            phone_number=self.PHONE_NUMBER,
            password=self.PASSWORD,
        )
        self.assertTrue(user.is_superuser)

    def test_can_create_staff(self):
        user = get_user_model().objects.create_user(
            phone_number=self.PHONE_NUMBER,
            password=self.PASSWORD,
            user_type=STAFF
        )
        self.assertTrue(user.user_type, 'S')
