#!/bin/bash

#   build.sh: build environment with virtualenv (Python), buildout (app)
#       
#       1. Python: use virtualenv with requirements.txt
#           - THIS SCRIPT BUILDS YOU A virtualenv called 'python27' in this dir
#           - recommended: install pyenv (e.g. from homebrew),
#           - then install Python 2.7.18 with pyenv
#           - then ensure you pyenv has virtualenv, pip
#       
#       2. Plone 4.3 Application deployment build with:
#           * 4 ZServer instances
#           * A debug instance
#           * RelStorage with PostgreSQL backend
#           * memcached, libmemcached, pylibmc for RelStorage
#           * Varnish
#           * HAProxy
#           * Psycopg2, lxml, and other Python libraries
#           * Test runners and coverage
#           * supervisor to control all long-running processes
#
#       Assumption: this buildout takes care of everything but the front-end
#                   web server for you; proxy from nginx|apache provided
#                   by your operating system to the Varnish included here.
#
#                   nginx -> varnish -> haproxy ==> zope(s)
#
#                   * Can and should be extended with a site.cfg; see 
#                     app/src/build/site.cfg.example
#
#                   * This buildout is run and tested on 64bit
#                     Linux and Mac OS X.

# some paths necessary for execution
BUILD_ROOT=$(dirname $0)
if [ "$BUILD_ROOT" == "." ]; then
    BUILD_ROOT=$(pwd)
fi
APP_ENV=$BUILD_ROOT/python27
APP_PYTHON="$APP_ENV/bin/python"

# buildout for Application Python, libraries; bootstrapped via system Python
echo "=== CREATING PYTHON VIRTUAL ENVIRONMENT, INSTALLING LIBS FROM PYPI  ==="
# pyenv or other python makes virtualenv
python2.7 -m virtualenv python27
# virtualenv python installs requirements in virtualenv:
$APP_PYTHON -m pip install -r requirements.txt

# buildout for application server / hosting stack
echo "=== BUILDING APPLICATION SERVER STACK BUILDOUT ==="
cd $BUILD_ROOT/app

if [ -f site.cfg ]; then
    $APP_ENV/bin/buildout -N -c site.cfg
else
    $APP_ENV/bin/buildout -N -c app.cfg
fi

echo "=== DONE WITH BUILDOUTS. ==="
exit 0
