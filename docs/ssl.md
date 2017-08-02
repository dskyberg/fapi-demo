# Managing SSL and OAuth certs and keys
The data for all certs and keys is in the [conf.d/ssl.d](conf.d/ssl.d) folder.

## SSL Configuration Files

### 01.conf.yaml
Here you can
change the location under `build` where the data will be generated, as well as
some default DN values

### 02.cas.yaml
All CA's, including the self signed root, are defined here.  Currently, there is
an intermediate CA (signed by the root CA) for each pseudo business entity.  So,
you shouldn't need to add a new CA unless you add an additional business entity.
Otherwise, you should be able to just change the existing values.

### 03.certs.yaml
This name is a bit misleading, but it contains definitions for all server and user
SSL certs that are signed by the various CA's.

## SSL Dependency Management
If you make SSL changes,  you can re-build the
SSL certs by running:

```bash
> ./run.sh -t create_ssl
```
- If you remove a `.key` file, the associated `.csr` file will be updated (or the
`.crt` file for the root, self signed CA)
- If you remove a `.csr` file, the associated `.crt` file will be updated
- If a `.crt` file for a CA is updated, all `.crt` files signed by that CA will
also be updated.
- If you change any `dn` attributes in the above files, the associated `.csr` or
`.crt` (for self signd) files will be updated

If you want to clean and rebuild all SSL data, run:
```bash
> ./run.sh -t clean_ssl,build_ssl
```
**REMEMBER:  CHANGING SSL REQUIRES REBUILDING DOCKER IMAGES**
