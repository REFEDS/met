import unittest

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from met.metadataparser.models import Federation
from met.metadataparser.tests import TestCase


class FederationTestCase(TestCase):

    def _test_federation_add(self):
        url = reverse('federation_add')
        response = self.client.post(url, {
            'name': 'Test federation',
        }, format='json')
        return response

    def test_federation_cannot_be_added_anon_user(self):
        self.assertEqual(Federation.objects.count(), 0)
        response = self._test_federation_add()
        self.assertFalse(response.url.endswith('?update=true'))
        self.assertEqual(Federation.objects.count(), 0)

    def test_federation_can_be_added_auth_user(self):
        self.login_as_admin_user()
        self.assertEqual(Federation.objects.count(), 0)
        response = self._test_federation_add()
        self.assertTrue(response.url.endswith('?update=true'))
        self.assertEqual(Federation.objects.count(), 1)
        federation = Federation.objects.first()
        self.assertEqual(federation.name, 'Test federation')

    def _test_federation_edit(self, add_editor=False):
        self.assertEqual(Federation.objects.count(), 0)
        federation = Federation.objects.create(
            name='Test federation'
        )
        if add_editor:
            federation.editor_users.add(self.user)
            permission = Permission.objects.get(
                codename='change_federation',
            )
            self.user.user_permissions.add(permission)
        url = reverse('federation_edit', args=[federation.slug])
        response = self.client.post(url, {
            'name': 'Modified test federation'
        }, format='json')
        self.assertEqual(Federation.objects.count(), 1)
        federation.refresh_from_db()
        return response, federation

    def test_federation_can_be_edited_admin_user(self):
        self.login_as_admin_user()
        response, federation = self._test_federation_edit()
        self.assertTrue(response.url.endswith('?update=true'))
        self.assertEqual(federation.name, 'Modified test federation')

    def test_federation_can_be_edited_editor_user(self):
        self.login_as_user()
        response, federation = self._test_federation_edit(add_editor=True)
        self.assertTrue(response.url.endswith('?update=true'))
        self.assertEqual(federation.name, 'Modified test federation')

    @unittest.skip('Skip until the permission system is fixed for federations')
    def test_federation_cannot_be_edited_regular_user(self):
        self.login_as_user()
        response, federation = self._test_federation_edit()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(federation.name, 'Test federation')
