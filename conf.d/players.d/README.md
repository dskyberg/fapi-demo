 # FAPI Demo Players and Service Configuration
Players represents the key Open Banking actors.  Each file under [confi.d/players.d](../conf.d/players.d)
represents a real world organization, or business.

The key values under each player are:
- Player meta data:
    - id: For reverse dict lookups.  Must be the same value as the players key.
    - name: Human readable name, and value for the CA's organizationName
    - domain: DNS domain that will be listed in dnsmasq
    - cidr: CIDR block used for dnsmasq.  Absent if the player has no services.
    - address: [OPTIONAL] If present, these attributes ovverride the default address
      in [SSL config](../conf.d/ssl.d/01.conf.yml) for all purposes, such as
      DN attributes, and web app 'About' pages.
    - ssl: SSL parameters for the player's  [CA](ca).

- [Player Services](#player-services)
- [Player Users](#player-users)

## Player Services
A player generally has a set of service endpoints that are accessed by other players.
Each service entry will become a docker container that provides those endpoints.

The key values under each `services` entry are:
- name: The lookup key for variable creation in Ansible.
- dns: If present, this service will be configured to use DNS.  There are two subelements:
    - hostname: The hostname given to the service.  If not present the service name is used.
    - ip: The IP address to append to the player's CIDR range, and used as the container's IP.
- ssl: Same as for the player, but for a server cert. If present, SSL data is
  copied to the services context.

## Player Users
Users represents customer account holders for the player. If the player is an IDP,
such as an email provider (ie, Google), then the user may also have a client SSL
certificate.

The key values under each `users` entry are:
- id: The account holder's id.  Defaults to a random UUID value
- first_name: First name of the user
- last_name: Last name of the user
- [OPTIONAL] email: Override the default `{{ first_name  }}.{{ last_name}}@{{ player.domain }}`
- [OPTIONAL] commonName. If not present, the email is used as the commonName
- ssl: Same as for service level `ssl`.  Overrides SSL defaults.

