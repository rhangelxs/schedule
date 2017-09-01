from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

@python_2_unicode_compatible
class Doctor(models.Model):
    name = models.CharField(_('Name'), blank=True, max_length=255)

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse('users:detail', kwargs={'username': self.username})

def next_hour():
    time = datetime.now()
    time = time.replace(minute=0, second=0, microsecond=0)
    return time + timedelta(hours=1)

@python_2_unicode_compatible
class Consultation(models.Model):
    date = models.DateTimeField(blank=False)
    doctor = models.ForeignKey(Doctor, blank=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)

    def __str__(self):
        return "%s %s" % (self.date, self.doctor)

    class Meta:
        unique_together = (("date", "doctor"),)

    def clean_fields(self, exclude=None):
        if self.date:
            # Check day
            if self.date.weekday() > 5:
                raise ValidationError({'date': "Specify day from Monday to Friday"})
            if self.date < next_hour():
                raise ValidationError({'date': "Time is already pass"}, code="datetime_before_now")
            if self.date.hour not in range(9, 18):
                raise ValidationError({'date': "Non working hours"}, code="nonworking_time")
        else:
            raise ValidationError({'date': 'No date specified'})
