Translation
===========

The PyCon site is set up for use in English and French, for the most part.

To disable the features documented here, change the USE_I18N setting to False.

Which language is displayed
---------------------------

By default, the request headers control which language is displayed. A user
can change their brower's settings to say what their preferred languages are,
and if French comes before English, the site will use French when available.
It'll fall back to English for text that isn't translated.

A language selector is displayed on the Dashboard page. This
allows a user to temporarily override the displayed language for the current
session.

Translating
-----------

For CMS pages, there are two body fields. The first is for English. The second
is for French. You'll have to scroll down a ways to see it when editing a CMS
page.

Text on most other pages, forms, etc is translatable using Django's
internationalization support. To add or update translations, a developer
would:

* set up a local development environment for PyCon according to the README
* make a new branch off the `develop` branch
* make sure you have Gnu gettext installed
* install fabric: ``pip install fabric``
* run ``fab make_messages`` to update the .po files, in case any translatable
  text has changed
* edit ``locale/fr/LC_MESSAGES/django.po``, filling in ``msgstr`` with the
  translated version of whatever text is in the ``msgid`` just above it.
* run ``fab compile_messages`` to update the .mo file with the new
  translations
* commit the updated .po and .mo files
* open a pull request against the main repo to get your updates included

If a non-developer is going to help with translation, a developer could
do all the steps except editing the .po file, just sending the .po file
to the translator for them to edit and send back.

Any text not translated in the translation files will be displayed as English.
