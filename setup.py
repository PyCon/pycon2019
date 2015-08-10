from distutils.core import setup


setup(
    name='pycon',
    version='2016',
    packages=['pycon', 'pycon.profile', 'pycon.schedule', 'pycon.sponsorship',
              'pycon.sponsorship.management',
              'pycon.sponsorship.management.commands',
              'pycon.sponsorship.templatetags', 'pycon.registration',
              'markedit', 'symposion', 'symposion.cms', 'symposion.boxes',
              'symposion.boxes.templatetags', 'symposion.teams',
              'symposion.teams.templatetags', 'symposion.utils',
              'symposion.reviews', 'symposion.reviews.management',
              'symposion.reviews.management.commands',
              'symposion.reviews.templatetags', 'symposion.schedule',
              'symposion.speakers', 'symposion.speakers.management',
              'symposion.speakers.management.commands', 'symposion.proposals',
              'symposion.proposals.templatetags', 'symposion.conference',
              'symposion.social_auth', 'symposion.social_auth.pipeline'],
    url='https://github.com/pycon/pycon/',
    license='LICENSE',
    maintainer='Caktus Consulting Group',
    maintainer_email='pycon@caktusgroup.com',
    description=''
)
