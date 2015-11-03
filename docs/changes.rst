Change Log
==========

This change log only goes back to partway-through development
for the 2016 Pycon.

The most recent update is at the top.

Version numbers are tags in git.  ``#`` numbers are issues and
pull requests in github (https://github.com/pycon/pycon.git).

Version 2016.15
---------------

Tuesday, November 3, 2015

* Fix buttons under sponsor carousels on CMS page (#576, #577)
* More export changes from njl (#574)

Version 2016.14
---------------

Tuesday, October 6, 2015

* Fix speaker photo uploads with non-ASCII filenames (#573)
* Change from Ned Jackson Lovely (njl): "richer API response" (#572)

Version 2016.13
---------------

Tuesday, September 29, 2015

* Add missing permissions for all kinds of proposals (#571)

Version 2016.12
---------------

Thursday, September 24, 2015

* Fix scrollbar on homepage images (#566, #567)
* Upgrade to mainline django-constance (#563)
* Final front-end tweaks (#558, #559):
  * added breadcrumbs the sponsor page, fixed double underline on active
    nav item, and changed H1 on venue pages to title case
  * When I click on a nav heading, its underline becomes twice as thick
    and the whole site content drops by one or two pixels, then when I
    click again to close the nav menu the whole site moves up again.
* Don't redirect / anymore. (#556)
* Remove "2015" from tutorials text on front page (#561)

Version 2016.11
---------------

Wednesday, September 23, 2015

* Bug fixes for Education Summit Proposals (#551, #552, #547, #548)
* Redirect / to sponsor prospectus (#546)
* Fix for uploading PDFs of financial aid receipts (#549, #550)
* Add Caktus logo to footer (#525, #555)
* Update Pycon favicon (#525, #555)
* Upgrade pytz (#553)

Version 2016.10
---------------

Wednesday, September 16, 2015

* Bug fix for Education Summit Proposals (#539, #540)
* Implement changes for some financial aid feedback (#508):

- [x] Python Experience Level: Should be a dropdown.
- [x] Sorting only sorts the names on the current page in review financial aid appellations page, not all.
- [x] Sorting doesn't sort correctly (we tried sorting date by see screenshot. Date field is being sorted lexicographically) (even when sorting just the names on the current page.)
- [x] "Grant letter sent" should have a drop-down Yes/No menu
- [x] "Cash check" should be called payment type
- [x] Travel Cash Check should go away.

* Changes to page nav/header and CMS styling (#537)

- [x] Fix navbar overlapping account links
- [x] Change account bar background and nav bar link padding
- [x] Fix navigation and breadcrumb issues

Version 2016.9
--------------

Tuesday, September 15, 2015

* Bug fix for CSS compression on deployed servers (f3b4950)

Version 2016.8
--------------

Thursday, September 10, 2015

* Fix missing image (#524, #530)
* Redirect from homepage to sponsor prospectus page (temporary) (#532)
* Send emails when presentations are saved in the admin (#496, #402)
* Add proposal type for education summit (#494, #521)

Version 2016.7
--------------

Thursday, September 3, 2015

* Fix grammar in fixture that creates volunteers team (#522)
* CMS page fixes (#506, #519):

    Nav
    * [x] Just above 980px the logo is needs to be centered in between the edge of the screen and the navigation. It is currently to close to the nav.
    * [x] The “you are here” underline in the mockup nav bar (a) is tightly attached beneath its word, (b) does not stick out from under its word in either direction, and (c) is several pixels high to give it weight and to visually match the stroke width of the nice and weighty font. The line is too far beneath the word, and sticks out awkwardly to the right. It should be made to match the mockup if possible.

    Breadcrumbs
    * [x] The green breadcrumb container needs to be shorter and match the mockup i.e. less space above and below the breadcrumb text.
    * [x] Use Roboto Condensed Bold for the breadcrumb font.

* Nav and account bar fixes (#504, #507):

    * [x] Align the bottom of the main nav links with the bottom of the copy in the account buttons.
    * [x] Make account bar links Title case.
    * [x] Change main nav font family from Open Sans to Roboto Condensed.

* Home page design updates (#505, #514):

    Motto:
    * [x] The top and bottom rules should be 80% of the width of the text.
    * [x] Need more space between the top and bottom rules and the motto text.
    * [x] The font size should be larger, and the line height should be shorter.

    City Skyline:
    * [x] Double check that the color of the city image and the tan background of the main content section are exactly the same color they are currently slightly different and that must be corrected.

* Display social login links (#441)
** On login page
** On settings/associations page
* Fix styling on finaid confirm buttons (#517, #518)
* Speed up review pages (lists of proposals for review) (#469)
* Fix rendering of proposal table on review pages to be beside
  the sidebar (#482, #515)
* Move all email addresses to settings from code (#502)
* Registration banner (#477, #478)
** The register now banner on the home page needs to be wider to accommodate more copy in the link.

Version 2016.6
--------------

Monday, August 24, 2015

* Clean up requirements (#489)
* Django 1.8.4 (#490)
* API to return session chair & runner data (#390, #484):
* Update organizer email address (#492)
* Add all APIs to the API docs (#392, #491)
* Special event model (#397, #398, #399, #400)
* Make page cache separate from session cache (#493)
* Completely disable French (#497)
* Add help for URL field (#500)
* Add box for intro text on venues page above hotels (#501)
* Fix bulk email test (#499)

Version 2016.5
--------------

Tuesday, August 18, 2015

* New dashboard buttons for applicants to accept, reject,
  withdraw, etc. their financial aid applications (#433, #385)
* Fix for tables not displaying on two pages (#485)
* Fix for sending tutorial emails (#488)
* Fix for changing status of single proposals (#487)
* Fix dropdown menus displaying below sponsor area (#479, #480)
* Enable persistent database connections for performance (#481)

Version 2016.4
--------------

Friday, August 14, 2015

* Send tutorial mass emails in the background (#393, #455)
* Django 1.8 (#473)
* Updates for continuous integration with Travis CI (#476)
* Move homepage login/logout buttons to upper right corner
  like the rest of the pages (#467, #474)
* Small test fix (#475)

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
