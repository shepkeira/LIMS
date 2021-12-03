from django.test import TestCase
from django.contrib.auth.models import User

from accounts.views import login_success

from accounts.models import *
from laboratory.models import *
from orders.models import *

class viewTestCase(TestCase):
    def setUp(self):
        # Create test user
        test_user = User.objects.create_user(username='testuser', password='asdf')
        test_user.save()
        

    #def test_login_success(self):
     #   """Test login_success() in accounts/views.py"""
#
 #       response = self.client.login(username='testuser', password='asdf')
  #      
   #     self.assertRedirects(response, 'accounts:customer_home_page')
