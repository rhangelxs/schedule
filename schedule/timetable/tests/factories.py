import factory

class DoctorFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'doctor-{0}'.format(n))

    class Meta:
        model = 'timetable.Doctor'
