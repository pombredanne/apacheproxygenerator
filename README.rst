Apache proxy file generator
===========================

Small tool for internal use at `Nelen & Schuurmans
<http://www.nelen-schuurmans.nl>`_ (but it might be useful as an example for
others).

Place a ``.ini`` file somewhere (suggestion: ``/etc/apache2/``) and place
sites in there, grouped by server::

    [p-web-ws-00-d04.external-nens.local]
    demo.lizard.net
    almere.lizard.net
    www.deltaportaal.nl

    [s-web-ws-00-d3.external-nens.local]
    test.almere.lizard.net

Call the ``generate_proxy.py`` script and give it the ini file and a conf file
as output location. The conf file will be replaced if it already exists. The
output will look like::

    # Lizard Web demo.lizard.net on p-web-ws-00-d04.external-nens.local
    <VirtualHost *:80>
        ServerName demo.lizard.net
        ProxyPreserveHost On
        ProxyPass / http://p-web-ws-00-d04.external-nens.local/
        ProxyPassReverse / http://p-web-ws-00-d04.external-nens.local/
    </VirtualHost>
    # Permanent redirect from www.* to the without-www domain.
    <VirtualHost *:80>
        ServerName www.demo.lizard.net
        RewriteEngine On
        RewriteRule  "^(.*)" "http://demo.lizard.net$1" [R=301,L]
    </VirtualHost>

So two things happen per site:

- The requests are proxied to the server under which header you placed the DNS
  name.

- A ``www.`` is prepended and given a permanent redirect to the non-www
  site. Note that this is reversed in case you yourself place a www site name
  in there.

It is handy to place a script somewhere (suggestion:
``/usr/local/bin/generate_proxy``) with a content like this::

    #!/bin/sh
    INI=/etc/apache2/generated_proxy.ini
    CONF=/etc/apache2/sites-available/generated_proxy.conf
    /root/apacheproxygenerator/generate_proxy.py $INI $CONF
    apache2ctl configtest
    echo "If succesful, run 'apache2ctl graceful'"

