Translation
===========

The PyCon site is set up for use in English and French, for the most part.

For CMS pages, there are two body fields. The first is for English. The
second is for French. You'll have to scroll down a ways to see it when
editing a CMS page.

The French body will be used on the site if it's not empty and if the user's
browser's request headers say to prefer French over English.

Text on most other pages, forms, etc is translatable. To add or update
translations, a developer would:

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
