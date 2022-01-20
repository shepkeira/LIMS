# Django
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class accountsUserTagsTestCase(TestCase):
    def setUp(self):
        self.client_group = Group.objects.create(name='Client')
        self.emp_group = Group.objects.create(name='Employee')
        self.admin_group = Group.objects.create(name='Admin')
        self.test_user_client = User.objects.create_user(
            username='testuser_c', password='asdf')
        self.test_user_client.groups.add(Group.objects.get(name='Client'))
        self.test_user_emp = User.objects.create_user(
            username='testuser_e', password='asdf')
        self.test_user_emp.groups.add(Group.objects.get(name='Employee'))
        self.test_user_admin = User.objects.create_user(
            username='testuser_a', password='asdf')
        self.test_user_admin.groups.add(Group.objects.get(name='Admin'))
        self.test_user_anon = User.objects.create_user(
            username='testuser', password='asdf')

    def test_has_group(self):
        self.assertEqual(self.test_user_client.groups.filter(
            name='Client').exists(), True)
        self.assertEqual(self.test_user_emp.groups.filter(
            name='Employee').exists(), True)
        self.assertEqual(self.test_user_admin.groups.filter(
            name='Admin').exists(), True)
        self.assertEqual(self.test_user_anon.groups.filter(
            name='Client').exists(), False)
        self.assertEqual(self.test_user_anon.groups.filter(
            name='Employee').exists(), False)
        self.assertEqual(self.test_user_anon.groups.filter(
            name='Admin').exists(), False)
