# Django
from django.test import TestCase
from django.contrib.auth.models import User

# Third-party libraries
from model_bakery import baker
from model_bakery.recipe import Recipe

# Our apps
from accounts.models import *
from accounts.views import *
from laboratory.models import *
from laboratory.views import *
from laboratoryOrders.models import *
from laboratoryOrders.views import *
from orders.models import *
from orders.views import *


class laboratoryViewsTestCase(TestCase):
    def setUp(self):
        self.test_user_client = User.objects.create_user(
            username='testuser_c', password='asdf')
        self.test_user_emp = User.objects.create_user(
            username='testuser_e', password='asdf')

        self.test_client = baker.make_recipe(
            'accounts.client_recipe',
            user=self.test_user_client
        )

        self.test_labworker = baker.make_recipe(
            'accounts.labworker_recipe',
            user=self.test_user_emp
        )

        self.sample = baker.make(Sample)
        self.order_sample = baker.make(OrderSample, sample = self.sample)

    def test_lab_home_page_unauth(self):
        # Unauthenticated user
        response = self.client.get('/laboratory/home_page/')
        self.assertRedirects(response, '/')

    def test_lab_home_page_lab_worker(self):
        # Authenticated lab worker
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/home_page/')
        self.assertEqual(response.status_code, 200)  # 200 means no redirect

    def test_lab_home_page_client(self):
        # Other user type
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/home_page/')
        # Hard to track redirection path here, so just check it did redirect somewhere
        self.assertEquals(response.status_code, 302)

    def test_sample_list(self):
        # Authenticated lab worker
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/sample_list/')
        self.assertEqual(response.status_code, 200)  # 200 means no redirect

        # Unauthenticated user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/sample_list/')
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/sample_list/')
        self.assertEqual(response.status_code, 302)

    def test_read_barcode(self):
        # Authenticated lab worker
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/read_barcode/')
        self.assertEqual(response.status_code, 200)  # 200 means no redirect

        # Unauthenticated user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/read_barcode/')
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/read_barcode/')
        self.assertEqual(response.status_code, 302)

    def test_view_barcode(self):
        # Authenticated lab worker
        self.client.login(username='testuser_e', password='asdf')
        sample_id = Sample.objects.all().first().id
        response = self.client.get('/laboratory/barcode/'+ str(sample_id) +'/')
        self.assertEqual(response.status_code, 200)  # 200 means no redirect

        # Unauthenticated user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/barcode/'+ str(sample_id) +'/')
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/barcode/'+ str(sample_id) +'/')
        self.assertEqual(response.status_code, 302)

    def test_ready_for_distribution(self):
        # Authenticated user
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/distribution/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/distribution.html')

        # Unauthenticaed user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/distribution/')
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/distribution/')
        self.assertEqual(response.status_code, 302)

    def test_create_lab_sample(self):
        # Authenticated user
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/distribute_sample/' + str(self.sample.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/distribute_sample.html')

        # Unauthenticaed user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/distribute_sample/' + str(self.sample.id))
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/distribute_sample/' + str(self.sample.id))
        self.assertEqual(response.status_code, 302)
    
    def test_order_list(self):
        # Authenticated user
        self.client.login(username='testuser_e', password='asdf')
        response = self.client.get('/laboratory/order_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/order_list.html')

        # Unauthenticaed user or authenticated client
        self.client.logout()
        response = self.client.get('/laboratory/order_list/')
        self.assertRedirects(response, '/')
        self.client.login(username='testuser_c', password='asdf')
        response = self.client.get('/laboratory/order_list/')
        self.assertEqual(response.status_code, 302)
