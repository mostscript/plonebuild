UPIQ buildout
=============

This is a Plone buildout for UPIQ projects.  It aims to include Python 2.7
and an application stack build for Plone including:

* Multiple instances of Zope/ZServer
* varnish + haproxy front end
* PosgreSQL and Memcached for use by RelStorage back-end.
* UPIQ and third-party add-ons, customizations
* Application service control via supervisord

Contains Python build sub-tree from github.com/collective/buildout.python
(GPL v2 licensed).

All content herein (excepting the python/ directory)
is licensed under an MIT-style license (see COPYING.txt).

