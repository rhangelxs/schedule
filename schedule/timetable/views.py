import calendar

from django.core.urlresolvers import reverse
from django import forms
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic import edit

from django.contrib.auth.mixins import LoginRequiredMixin

from schedule.timetable.models import Consultation, next_hour

from datetime import timedelta

from django.utils.datetime_safe import datetime
from django.forms import widgets

class ConsultationDetailView(LoginRequiredMixin, DetailView):
    model = Consultation
    slug_field = 'pk'
    slug_url_kwarg = 'pk'


class ConsultationRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # TODO extract values to settings
        hours = [(hour, "%s-%s" % (hour, hour+1)) for hour in range(9, 18)]
        days = [(day, day) for day in range(1, 32)]
        months = [(i+1, month) for i, month in enumerate(calendar.month_abbr[1:])]
        current_year = datetime.now().year
        years = [(year, year) for year in range(current_year, current_year + 4)]

        # TODO Add some styling and default values
        # or change to SplitDateTimeWidget
        _widgets = (
            widgets.Select(attrs=attrs, choices=hours),
            widgets.Select(attrs=attrs, choices=days),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.day, value.month, value.year]
        return [None, None, None, None]

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = datetime(
                hour=int(datelist[0]),
                day=int(datelist[1]),
                month=int(datelist[2]),
                year=int(datelist[3]),
            )
        except (ValueError, TypeError):
            return ''
        else:
            return D

class ConsultationEditForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['doctor', "date"]
        exclude = ["client"]

    date = forms.DateTimeField(widget=DateSelectorWidget, initial=next_hour())


class ConsultationUpdateView(LoginRequiredMixin, edit.CreateView):

    form_class = ConsultationEditForm
    model = Consultation

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super(ConsultationUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('timetable:detail',
                       args=(self.object.pk,))



class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation

    def get_queryset(self):
        # Filter only current user
        return Consultation.objects.filter(client=self.request.user)
