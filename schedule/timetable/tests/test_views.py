from django.test import RequestFactory

from test_plus.test import TestCase

from schedule.timetable.tests import factories

from ..views import (
    ConsultationUpdateView,
    ConsultationEditForm)


class BaseTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.doctor = factories.DoctorFactory.create()
        self.factory = RequestFactory()



class TestEmptyUpdateView(BaseTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestEmptyUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = ConsultationUpdateView()
        self.form = ConsultationEditForm
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request


    def test_init_without_entry(self):
        self.assertFalse(self.form(data={}).is_valid())

class TestDatesInUpdateForm(TestEmptyUpdateView):
    def setUp(self):
        super(TestDatesInUpdateForm, self).setUp()

    def test_init_with_next_date(self):
        form = self.form({"doctor": self.doctor.pk, "date_0": 12, "date_1": 12, "date_2": 12, "date_3": 2018})
        self.assertEqual(form.errors, {})
        self.assertTrue(form.is_valid())

    def test_init_with_next_sunday(self):
        form = self.form({"doctor": self.doctor.pk, "date_0": 0, "date_1": 7, "date_2": 1, "date_3": 2018})
        self.assertEqual(len(form.errors), 1)
        self.assertFalse(form.is_valid())

    def test_init_with_wrong_time(self):
        form = self.form({"doctor": self.doctor.pk, "date_0": 0, "date_1": 12, "date_2": 12, "date_3": 2018})
        self.assertEqual(len(form.errors), 1)
        self.assertFalse(form.is_valid())

    def test_init_with_passed_date(self):
        form = self.form({"doctor": self.doctor.pk, "date_0": 12, "date_1": 12, "date_2": 12, "date_3": 2016})
        self.assertEqual(len(form.errors), 1)
        self.assertFalse(form.is_valid())
