from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from ..constants import STAFF


class TestAdminViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_admin_login_page(self):
        res = self.client.get(reverse_lazy('core:admin_login'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'core/admin/login.html')
        self.assertContains(res, 'csrfmiddlewaretoken')

    def test_cannot_login_to_admin_with_invalid_credentials(self):
        res = self.client.post(
                reverse_lazy('core:admin_login'),
                {'phone_number': '1111111111', 'password': 'random'}
            )
        self.assertEqual(res.status_code, 302)

    def test_login_to_admin_with_valid_credentials(self):
        user = get_user_model().objects.create_user(
            phone_number='9999999999',
            password='password',
            user_type=STAFF
        )
        res = self.client.post(
                reverse_lazy('core:admin_login'),
                {'phone_number': user.phone_number, 'password': user.password}
        )
        self.assertEqual(res.status_code, 302)

    def test_cannot_access_admin_dashboard_page_without_auth(self):
        res = self.client.get(reverse_lazy('core:admin_dashboard'))
        self.assertEqual(res.status_code, 302)

    def test_admin_dashboard_page(self):
        user = get_user_model().objects.create_user(
            phone_number='9999999999',
            password='password',
            user_type=STAFF
        )
        self.client.force_login(user)
        res = self.client.get(reverse_lazy('core:admin_dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'core/admin/dashboard.html')
        self.assertContains(res, 'Dashboard | ZenWellness')
