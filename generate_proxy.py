#!/usr/bin/env python
import sys
from pprint import pprint

SITE_TEMPLATE = """
# Lizard Web {site} on {server}
<VirtualHost *:80>
    ServerName {site}
    ProxyPreserveHost On
    ProxyPass / http://{server}/
    ProxyPassReverse / http://{server}/
</VirtualHost>
# Permanent redirect from www.* to the without-www domain.
<VirtualHost *:80>
    ServerName www.{site}
    RewriteEngine On
    RewriteRule  "^(.*)" "http://{site}$1" [R=301,L]
</VirtualHost>

"""

def site_sort(a, b):
    """Sort sites 'reversely': so group .net and .nl together and so."""
    a = list(a)
    b = list(b)
    a.reverse()
    b.reverse()
    return cmp(a, b)


def main():
    if len(sys.argv) < 3:
        print("Usage: pass along source .ini file and target .conf arguments")
        sys.exit(1)
    ini_file = sys.argv[1]
    apacheconf_file = sys.argv[2]

    print("Reading configuration from %s" % ini_file)
    ini_lines = [line.strip() for line in open(ini_file).readlines()]
    ini_lines = [line for line in ini_lines if line]
    ini_lines = [line for line in ini_lines if not line.startswith('#')]
    sites = {}
    server = None
    for line in ini_lines:
        if line.startswith('['):
            line = line.strip('[]')
            server = line.strip()
            continue
        site = line
        sites[site] = server
    pprint(sites)

    apacheconf = open(apacheconf_file, 'w')
    site_names = sites.keys()
    site_names.sort(cmp=site_sort)
    # First print some handy overview text.
    apacheconf.write("# Sites in the order in which they appear:\n")
    for site in site_names:
        apacheconf.write("# - %s\n" % site)
    hosts = list(set(sites.values()))
    hosts.sort()
    apacheconf.write("#\n# Servers with their sites:\n")
    for host in hosts:
        apacheconf.write("# Host %s\n" % host)
        for site in site_names:
            if sites[site] == host:
                apacheconf.write("# - %s\n" % site)
        apacheconf.write("#\n")

    for site in site_names:
        server = sites[site]
        site_config = SITE_TEMPLATE.format(site=site, server=server)
        apacheconf.write(site_config)
        print("Wrote config for %s." % site)
    apacheconf.close()


if __name__ == '__main__':
    main()

