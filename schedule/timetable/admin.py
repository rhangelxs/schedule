from django.contrib import admin
from schedule.timetable.models import *

admin.site.register(Doctor)

class ConsultationAdmin(admin.ModelAdmin):
    model = Consultation

    list_display = ('date'
                    , 'doctor'
                    , 'client'
                    )
    list_filter = ("doctor",)
    ordering = ['-date']


admin.site.register(Consultation, ConsultationAdmin)
