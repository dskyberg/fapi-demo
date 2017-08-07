# SSL Configuration

## Managing SSL and OAuth certs and keys
The configuration data for all certs and keys is contained in the player
configs, unders SSL.  If not specified there, the default settings, in
[01.conf.yml](01.conf.yml) are used.

## SSL Configuration File: [01.conf.yml](01.conf.yml)
Contains the following sections:
### dir
This is the the top level directory (under [project.buildDir](../conf.d/project.d/00.conf.yml))
where generated certs, keys, etc. are saved.

### exts
Default file extensions for the generated files.  You can change this i you have need.

### default_issuer
Each player has its own intermediate CA.  By default it is signed by the CA listed
here, which is the self signed root CA.

### dn
These are the default values used anywhere DN attributes are required.

### root, intermediate, server, user
Specifies defaults for each type of cert.


## SSL Dependency Management
If you make SSL changes,  you can re-build the
SSL certs by running:

```bash
$ ./run.py -p ssl_only -t create_ssl
```
`create_ssl` will rebuild based on config and file dependency changes.

- If you remove or `touch` a `.key` file, the associated `.csr` file will be updated (or the
`.crt` file for the root, self signed CA)
- If you remove or `touch` a `.csr` file, the associated `.crt` file will be updated
- If a `.crt` file for a CA is removed or  or `touch`ed, all `.crt` files signed by that CA will
also be updated.
- If you change any `dn` attributes in the above files, the associated `.csr` or
`.crt` (for self signd) files will be updated

If you want to clean and rebuild all SSL data, run:
```bash
$ ./run.sh -t clean_ssl,build_ssl
```
**REMEMBER:  CHANGING SSL REQUIRES REBUILDING DOCKER IMAGES**
