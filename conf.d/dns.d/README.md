# DNS Configuration
A Docker network is created so that all the player services can run in an
isolated environment.  DNSMasq is used as the network-wide DNS nameserver.
The DNS configuration file is used to configure top level DNS settings for
the network.

The file [01.dns.yml](01.dns.yml) is used to manage this config.

## base_cidr
Set the first 16 bits of the IP addresses for the network.  It is currently set
to `172.25.0.0/16`.

## nameServer:
The DNS IP address given to each Docker container, and listed locally as its
nameServer.

## servers:
The upstream nameServers that DNSMasq will use if it can't resolve locally.