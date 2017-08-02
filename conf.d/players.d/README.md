 # FAPI Demo Players and Service Configuration
Players represents the key Open Banking actors.  Each file under `confi.d/players.d`
represents a real world organization, or business.

The key values under each player are:
- id: For reverse dict lookups.  Must be the same value as the players key.
- name: Human readable name, and value for the CA's organizationName
- domain: DNS domain that will be listed in dnsmasq
- cidr: CIDR block used for dnsmasq.  Absent if the player has no services.
- address: Address for all purposes, such as DN attributes, and web app 'About' pages.
- ssl: SSL parameters for that [CA](ca).

Each player has three subelements:
- [CA](player-ca)
- [Services](player-services)
- [Users](player-users)

## Player CA
The org will automatically have its own CA, signed by the global root CA.
The `ssl` key for the player is used to override default SSL cert values.

## Player Services
A player generally has a set of service endpoints that are accessed by other players.
Each service entry will become a docker container that provides those endpoints.

The key values under each `services` entry are:
- [key]: The lookup key for variable creation in Ansible.
- hostname: used with the player domain to create the DNS entry for the service.
- ssl: Same as for the player, but for a server cert. If set to `True`, then
the cert is signed by the player's CA, and defaults are used.  If absent,
or `False`, then no cert will be created for that service.

## Player Users
Users represents customer account holders for the player. If the player is an IDP,
such as an email provider (ie, Google), then the user may also have a client SSL
certificate.

The key values under each `users` entry are:
- id: The account holder's id.  Defaults to a random UUID value
- first_name: First name of the user
- last_name: Last name of the user
- email: Override the default `{{ first_name  }}.{{ last_name}}@{{ player.domain }}`
- ssl: Same as for service level `ssl`.  Should only be True for IDP players.

