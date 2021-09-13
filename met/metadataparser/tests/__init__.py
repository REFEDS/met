from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):

    def _login_with_user(self, user):
        self.client.login(username=user.username, password='met')

    def login_as_admin_user(self):
        self._login_with_user(self.admin_user)

    def login_as_user(self):
        self._login_with_user(self.user)

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@met.com',
            password='met',
        )

        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@met.com',
            password='met',
        )
