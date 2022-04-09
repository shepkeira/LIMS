"""
functions related to email notifications
"""
from django.core.mail import send_mail
from accounts.models import LabAdmin

class EmailNotifications:
    """
    Email Notification functions
    """
    from_email = 'lims0.system@gmail.com'

    def send_email_notification(self, to_emails, subject, body):
        """
        send email notification
        """
        send_mail(subject, body, self.from_email, to_emails, fail_silently=False)

    def admin_emails(self):
        """
        get all admin user emails
        """
        return [la.user.email for la in LabAdmin.objects.all()]

    def test_sample_notif(self, test_sample):
        """
        send notification when new test sample
        """
        user_email = test_sample.test_user().email
        to_emails = self.admin_emails()
        to_emails.append(user_email)

        order_number = test_sample.lab_sample_id.sample.order().order_number

        subject = f'New test sample created from order {order_number}'

        body = f"""
A new test sample for {test_sample.test} has been created from sample {test_sample.lab_sample_id.sample.id} in {test_sample.lab_sample_id.location}.

Please do not reply to this email.
                """
        self.send_email_notification(to_emails, subject, body)

    def sample_distributed(self, lab_sample):
        """
        send notification when new lab sample created
        """
        subject = 'New lab sample created from your order'
        body = f"""
Your sample has been assigned and distributed to the {lab_sample.location}

Please do not reply to this email.
                """
        to_emails = [lab_sample.lab_user().email]
        self.send_email_notification(to_emails, subject, body)

    def sample_inspected(self, inspection):
        """
        send notification when sample is inspected
        """
        subject = 'Inspection Received'
        body = f"""
Dear {inspection.sample.order().account_number.user.first_name},

Your {inspection.sample.sample_type} sample ID {inspection.sample.id} order #{inspection.sample.order().order_number} has been inspected by {inspection.inspector.first_name}.
Results:
    received quantity: {inspection.received_quantity}
    Package intact: {inspection.package_intact}
    Material intact: {inspection.material_intact}
    Inspection pass: {inspection.inspection_pass}

Please do not reply to this email.
                """
        to_email = [inspection.sample.sample_user().email]
        self.send_email_notification(to_email, subject, body)

    def test_result_notif(self, test_sample, result):
        """
        send notification when test results are inputed
        """
        sample_type = test_sample.lab_sample_id.sample.sample_type
        sample_id = test_sample.lab_sample_id.sample.user_side_id()
        subject = f'New test results on {sample_type} {sample_id}'
        body = f"""
Dear {test_sample.lab_sample_id.sample.order().account_number.user.first_name},

New test results for {test_sample.lab_sample_id}.
Status: {result.status}
Result: {result.result}
Test pass: {result.test_pass}

Please do not reply to this email.
                """
        to_email = [test_sample.test_user().email]
        self.send_email_notification(to_email, subject, body)

    def new_order_notif(self, order, new_ordertests):
        """
        send notification when a new order is placed
        """
        subject = f'New Order Received: {order.order_number}'
        body = f"""
A new order has been received:
Order number: {order.order_number}
Account Number: {order.account_number}
Submission Date: {order.submission_date:%Y-%m-%d %H:%M}
Tests Ordered:
{ ''.join(map(str,[ f'{new_order_tests.test_id}, ' for new_order_tests in new_ordertests ]))[:-1] }

Please do not reply to this email.
            """
        to_emails = self.admin_emails()
        self.send_email_notification(to_emails, subject, body)
