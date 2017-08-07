# Docker Image and Container Configuration
Every docker image and container that must be build and run must have a
corresponding configuration.

## Naming Conventions
Service descriptor files (under `conf.d/services.d) are typically named `<priority>.<player name>.d/<priority>.<service name>.yml`
Thus, the `db` descriptor for the `aspsp` player is in `conf.d/services.d/aspap.d/02.db.yml`.

## Priority Values
Every folder name and file name under `conf.d/services.d` starts with a 2 digit
priority value.  This value ensures that files are processed in dependency order.
The values do not need to be unique.  Just ensure that if one service depends on
another service, the priority value of the dependent service is higher than the
dependency service.

## Listing the Services
You can get a listing of all the service names by running:

```bash
$ scripts/list_services.py -r
dnsmasq
aspsp_db
aspsp_auth
aspsp_api
psu_idp_bob
```
