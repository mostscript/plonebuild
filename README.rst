UPIQ buildout
=============

This is a Plone buildout for Mostscript projects.  

It aims to include Python 2.7 and application stack build for Plone including:

* Multiple instances of Zope/ZServer
* varnish + haproxy front end
* PosgreSQL and Memcached for use by RelStorage back-end.
* Application packages and third-party add-ons, customizations
* Application service control via supervisord

Building Python
---------------

* Mac: install OpenSSL via Homebrew:

  - `$ brew install openssl`

  - Set LDFLAGS and CFLAGS in your profile or prior to executing
    the Python buildout:

    .. code-block:: bash

        export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future
        export LDFLAGS="-L/usr/local/opt/openssl/lib -L/usr/local/opt/zlib/lib"
        export CFLAGS="-I/usr/local/opt/openssl/include -I/usr/local/opt/zlib/include -L/usr/local/opt/openssl/lib -L/usr/local/opt/zlib/lib"
        export CPPFLAGS=-I/usr/local/opt/openssl/include


Rights and Attribution
----------------------

Contains Python build sub-tree from github.com/collective/buildout.python
(GPL v2 licensed).

All content herein (excepting the python/ directory) has title owned by its
author(s) and all, except Python build, licensed under an MIT-style license
(see COPYING.txt).

Copyright © 2018 Mostscript LLC
Copyright © 2010-2017 The University of Utah

