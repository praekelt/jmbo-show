Changelog
=========

next
----
#. Change the view modifier so it does not write directly to `extra_params`. This change causes template breakage if you have customized `show_detail.html`.

0.2.4
-----
#. Fix missing south dependency on `jmbo-calendar`.

0.2.3
-----
#. Cache show detail page.
#. Add a field so queries can be ordered on start time instead of start datetime.

0.2.2
-----
#. Change calculation for on air now.

0.2.1
-----
#. Missing imports added. Shows can now be set to be on Saturday or Sunday.

0.2
---
#. Refactor to be dependant on `jmbo-foundry`. This refactor is backwards incompatible, but since jmbo-show is not in widespread use yet it is not an issue.

0.0.6
-----

#. Added show contributor contact form, views and templates.

