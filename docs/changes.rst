Change Log
==========

This change log only goes back to partway-through development
for the 2016 Pycon.

The most recent update is at the top.

Version numbers are tags in git.  ``#`` numbers are issues and
pull requests in github (https://github.com/pycon/pycon.git).

Version 2016.3
--------------

Wednesday, August 12, 2015

* Undo bad last-minute migration fix.

Version 2016.2
--------------

Wednesday, August 12, 2015

* Fix sponsor logo download (#436)
* Update button colors (#470)
* Past Pycons slideshow (442)
* Combine site style files (#465)
* Add talk URLs (#389):

    TALKS/SESSION CHAIRS
    • Add the following fields to each talk slot:
    ⁃ Talk video URL
    ⁃ Talk slides URL
    ⁃ Talk assets URL
    ⁃ Those fields should exist in the /schedule/conference.json feed
    ⁃ There should be an API which I can use to update those URLs
    ⁃ it should be as simple as possible, since I'll call it from scripts
    ⁃ I don't care what it looks like, so long as I can call it with 3 lines
    of requests (ex, no oauth or anything complex)
    ⁃ Those fields should be editable from the django admin
    ⁃ If present and non-empty, they should be shown on the talk description page

    Set the video, slides, and assets URLs for a talk.

    Expects a POST, with an identifier for the talk as returned in
    the conf_key from the conference JSON API (/YYYY/schedule/conference.json)
    as part of the URL:

        http[s]://xxxxxxxxx/api/set_talk_urls/12345/

    and the request body a JSON-encoded dictionary with up to three keys:

      * video_url
      * slides_url
      * assets_url

    whose values are syntactically valid URLs.  The provided values will be
    set on the talk.

    Authentication is via an API key like other Pycon site APIs.

    :param conf_key: The 'conf_key' value returned for a slot by the conference
     JSON method.
    :returns: 202 status if successful


Version 2016.1
--------------

Monday, August 10, 2015

* Fix Google auth (#468)

Version 2016.0
--------------

Monday, August 10, 2015

* Fix ``fab server manage_run:dbshell``
* Add tests for thunderdome API (#432)
* Sponsor updates (#437, #438): display company description
  on sponsors page; remove company name benefit
* Numerous style updates
* Remove unused jquery.js file (#464)
* Allow selecting and changing the status of multiple proposals
  at once (#451)
* Turn off debug logging in production (#445)
* Use right version of django-reversion for our version of Django (#463)
* Change hosting credit from OSU OSL to Rackspace (#462)
* Include abstract contents in exports (#456)
* Clean up some warnings from more recent Djangos (#449)
* Add celery (#448)
* Add uploading of receipts for financial aid (#427, #382, #383)
* Add missing migration (#439)
* Updates to fabfile for PSF-infra changing to Salt (#434, #435)
* Update Raven to 5.5.0 (#335, #420)
* Google login (#375, #416)
* Updates to sponsor details (#379, #380)
* Multiple contact email addresses for sponsors (#413, #381)
* Improve README (#412)
* Update to Django 1.7 (#408)
* Upgrade Pillow to 2.9.0 (#407)
* Fab manage_run (#406)
* Update to Djanog 1.6 (#405)
* Fixes for the vagrant development environment (#404)
