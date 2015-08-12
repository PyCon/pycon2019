import factory
from symposion.speakers.models import Speaker


class SpeakerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Speaker
