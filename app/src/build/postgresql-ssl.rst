Purpose
=======

SSL can be enabled per-site for PostgreSQL in this buildout; here are
rough notes on the process.

Why?
====

In this buildout, normally communication to PostgreSQL is local over UNIX
domain sockets and possibly 127.0.0.1 (IPv4 localhost).

You may want to enable SSL as the only permitted vehicle for other source
IPv4 addresses to connect to PostgreSQL (e.g. for RelStorage in Zope
app server clients running on other hosts).

Overview
========

There is too much that is site-specific about maintaining SSL keys and
certificates, so this is disabled by default in buildout configuration;
however, hooks are provided to enable SSL in etc/postgresql.conf and
in etc/pg_hba.cfg as you see fit.

The process usually involves editing a site.cfg file (not checked into git)
with values to enable SSL and point to a CA certificate in 
etc/postgresql.conf -- this presumes you actually have keys and certificates
copied to the correct locations in the first place.

The next section describes key/certificate setup.

Process for keys and certificates
=================================

 * You will need a CA key and certificate to sign both client and server
   certificates with one common trusted authority.  This is best done
   out-of-band on a computer that is not a production server.

  * The CA key should be protected with a DES3 passphrase.

  * The CA key should not be copied to the server or the client, only
    used on the out-of-band machine to sign relevant signing requests for
    the client and server certificates.

  * The CA "root" certificate should be copied to both the client and the
    server, and the root certificate may be "chained" (concatenated) with
    the server certificate.

Basic steps (out-of-band computer with CA key):
-----------------------------------------------

::

  # create root/CA signing key (choose a passphrase):
  openssl genrsa -des3 -out root.key 2048
  chmod 600 root.key

  # create root certificate:
  openssl req -new -x509 -days 3650 -key root.key -out root.crt \
    -subj '/C=US/ST=Utah/L=Salt Lake City/O=University of Utah/OU=Department of Pedatrics/CN=upiq'

  # create server key for postgres server:
  openssl genrsa -des3 -out server.key 2048

  # strip the passphrase from the server key, and chmod it:
  openssl rsa -in server.key -out server.key
  chmod 600 server.key

  # create signing request using server key (to be signed in later step by root):
  openssl req -new -nodes -key server.key -days 3650 -out server.csr \
    -subj '/C=US/ST=Utah/L=Salt Lake City/O=University of Utah/OU=Department of Pedatrics/CN=postgres'

  # Use root/CA cert to sign certificate based on CSR:
  openssl x509 -days 3650 -req -in server.csr -CA root.crt -CAkey root.key \
    -CAcreateserial -out server.crt

  # create combined (chained) server, root certificates:
  cat server.crt root.crt > server-combined.crt

    ** NOTE ** --
    The server-combined.crt file will be renamed to server.crt when copied
    onto the PostgreSQL server's data directory.

  #------- CLIENT SIDE ------------

  # create client key for postgres client:
  openssl genrsa -des3 -out client.key 2048

  # strip the passphrase from the server key and chmod it:
  openssl rsa -in client.key -out client.key
  chmod 600 client.key

  # create a CSR using client.key using the 'qi' common name:
  openssl req -new -nodes -key client.key -days 3650 -out client.csr \
    -subj '/C=US/ST=Utah/L=Salt Lake City/O=University of Utah/OU=Department of Pedatrics/CN=qi'

  # sign certificate using root/CA cert:
  openssl x509 -days 3650 -req -in client.csr -CA root.crt -CAkey root.key \
    -CAcreateserial -out client.crt


Copying keys and certificates to servers
----------------------------------------

1. Copy root.crt, server_combined.crt, and server.key to data directory
   (var/postgres) of server; rename server_combined.crt to server.crt.

2. Enable configuration of PostgreSQL SSL in postgresql.conf and pg_hba.conf
   by editing respective settings in buildout pgconf and pghba parts in
   site.cfg (pgconf: ssl = on, ssl_ca_file points to root.crt; pghba: use
   `cert clientcert=1` in a hostssl line).

3. Test PostgreSQL to make sure things start, run okay with config.

4. Upload client.crt, client.key, and root.crt to ~/.postgresql on client
   machine.

5. Update iptables or firewall rules as needed, esp limiting if you use
   a host address of 0.0.0.0 in your site.cfg (the default is only
   localhost).


Example pg_hba line:
--------------------

::

  # SSL connections over IPv4 to plone4_zodb database
  hostssl plone4_zodb qi          0.0.0.0/0             cert  clientcert=1

