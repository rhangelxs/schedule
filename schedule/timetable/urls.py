from django.conf.urls import url

from schedule.timetable import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ConsultationListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.ConsultationRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<pk>[\w.@+-]+)/$',
        view=views.ConsultationDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.ConsultationUpdateView.as_view(),
        name='update'
    ),
]
