#!/bin/bash

#   build.sh: wrap buildouts contained for:
#       
#       1. Python
#           (based on collective.buildout.python)
#       
#       2. Plone 4.2 Application deployment build with:
#           * Two ZServer instances
#           * A debug instance
#           * RelStorage with PostgreSQL backend
#           * memcached, libmemcached, pylibmc for RelStorage
#           * Varnish
#           * HAProxy
#           * Psycopg2, lxml, and other Python libraries
#           * Test runners and coverage
#           * Dexterity
#           * supervisor to controll all your long-running processes
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
#                   * This buildout is run and tested on 32bit and 64bit
#                     Linux and Mac OS X.
#
#   Default is deployment buildout, for a tiny buildout, pass single
#   option --tiny

# some global constants
PYVER=2.7

# some paths necessary for execution
BUILD_ROOT=$(dirname $0)
if [ "$BUILD_ROOT" == "." ]; then
    BUILD_ROOT=$(pwd)
fi
SYSTEM_PYTHON=$(which python)
APP_PYTHON="$BUILD_ROOT/python/python-$PYVER/bin/python"

# buildout for Application Python, libraries; bootstrapped via system Python
echo "=== BUILDING PYTHON ENVIRONMENT AND LIBRARIES ==="
echo "    System Python: $SYSTEM_PYTHON"
cp $BUILT_ROOT/pysite_in.cfg $BUILD_ROOT/python/site.cfg
cd $BUILD_ROOT/python
$SYSTEM_PYTHON bootstrap.py --distribute
bin/buildout -N

# buildout for application server / hosting stack
echo "=== BUILDING APPLICATION SERVER STACK BUILDOUT ==="
cd $BUILD_ROOT/app
$APP_PYTHON bootstrap.py --distribute
if [ "$1" == "--tiny" ]; then
    echo "=== TINY/DEVELOPMENT-ONLY BUILDOUT REQUESTED ==="
    bin/buildout -N -c tiny.cfg
else
    echo "=== DEFAULT (production) BUILDOUT REQUESTED ==="
    bin/buildout -N -c buildout.cfg
fi

echo "=== DONE WITH BUILDOUTS. ==="
exit 0;

