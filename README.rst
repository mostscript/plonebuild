UPIQ buildout
=============

This is a Plone buildout for UPIQ projects.  It aims to include Python 2.7
and an application stack build for Plone including:

* Multiple instances of Zope/ZServer
* varnish + haproxy front end
* PosgreSQL and Memcached for use by RelStorage back-end.
* UPIQ and third-party add-ons, customizations
* Application service control via supervisord

Building Python
---------------

* Mac: as of OS X 10.11 (El Capitan), OpenSSL libraries are not included
  in the core Apple distribution of the OS.
  As such, use of homebrew openssl package is recommended, via:

  - `$ brew install openssl`

  - Set LDFLAGS and CFLAGS in your profile or prior to executing
    the Python buildout:

    .. code-block:: bash

        export LDFLAGS=-L/usr/local/opt/openssl/lib
        export CPPFLAGS=-I/usr/local/opt/openssl/include

Rights and Attribution
----------------------

Contains Python build sub-tree from github.com/collective/buildout.python
(GPL v2 licensed).

All content herein (excepting the python/ directory)
is licensed under an MIT-style license (see COPYING.txt).

Copyright © 2016 The University of Utah

