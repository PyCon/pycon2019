import factory
from symposion.speakers.models import Speaker


class SpeakerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Speaker
