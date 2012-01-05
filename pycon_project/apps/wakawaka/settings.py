from django.conf import settings

LOCK_CACHE_PREFIX = getattr(settings, "WAKAWAKA_LOCK_CACHE_PREFIX", "wwl")

LOCK_TIMEOUT = getattr(settings, "WAKAWAKA_LOCK_TIMEOUT", 60*60)

DEFAULT_INDEX = getattr(settings, 'WAKAWAKA_DEFAULT_INDEX', 'WikiIndex')

# Wiki slugs must been CamelCase but slashes are fine, if each slug
# is also a CamelCase/OtherSide
WIKI_SLUG = r'((([A-Z]+[a-z]+){2,})(/([A-Z]+[a-z]+){2,})*)'
WIKI_SLUG = getattr(settings, 'WAKAWAKA_SLUG_REGEX', WIKI_SLUG)
