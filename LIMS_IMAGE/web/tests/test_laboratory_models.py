from django.test import TestCase

from accounts.models import *
from laboratory.models import *
from orders.models import *

class laboratoryModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        testLocation = Location.objects.create(name='test location name', code='L')
        testTest = Test.objects.create(name='testTest', code='T', cost='1.23', rush='True', time_taken='1')
        # TODO add lab worker
        testSample = Sample.objects.create(sample_type='test sample type', sample_form='test sample form', sop_number='test sop number', lab_personal=)
        testLabSample = LabSample.objects.create(sample=testSample, lab_location=testLocation)
        testTestSample = TestSample.objects.create(lab_sample_id=testLabSample, test=testTest)
        testTestResult = TestResult.objects.create(status='test status', result='test result', test_id=testTestSample)

    def test_lab(self):
        tr = TestResult.objects.all().first()

        self.assertEqual(tr.status, 'test status')
