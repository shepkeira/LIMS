# Django
from unicodedata import name
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Third-party libraries
from model_bakery import baker
from model_bakery.recipe import Recipe


class accountsUserTagsTestCase(TestCase):
    def setUp(self):
        # Create test groups and users (client, employee, admin, and anonymous)
        self.client_group = baker.make_recipe(
            'accounts.group_recipe', name='Client')
        self.employee_group = baker.make_recipe(
            'accounts.group_recipe', name='Employee')
        self.admin_group = baker.make_recipe(
            'accounts.group_recipe', name='Admin')
        self.test_user_client = baker.make_recipe(
            'accounts.user_recipe', groups=[self.client_group])
        self.test_user_emp = baker.make_recipe(
            'accounts.user_recipe', groups=[self.employee_group])
        self.test_user_admin = baker.make_recipe(
            'accounts.user_recipe', groups=[self.admin_group])
        self.test_user_anon = baker.make_recipe('accounts.user_recipe')

    def test_has_group(self):
        # Asserts that user's group is of type Group
        self.assertIsInstance(self.test_user_client.groups.all()[0], Group)
        self.assertIsInstance(self.test_user_emp.groups.all()[0], Group)
        self.assertIsInstance(self.test_user_admin.groups.all()[0], Group)
        # Asserts if selected user has selected group
        self.assertTrue(self.test_user_client.groups.filter(
            name='Client').exists())
        self.assertTrue(self.test_user_emp.groups.filter(
            name='Employee').exists())
        self.assertTrue(self.test_user_admin.groups.filter(
            name='Admin').exists())

        # Asserts that anonymous user is not in any selected group
        self.assertFalse(self.test_user_anon.groups.filter(
            name='Client').exists())
        self.assertFalse(self.test_user_anon.groups.filter(
            name='Employee').exists())
        self.assertFalse(self.test_user_anon.groups.filter(
            name='Admin').exists())
