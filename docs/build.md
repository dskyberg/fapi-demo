# Build the System
Everything is scripted in Ansible, so building an running is easy!  However,
everything runs in Docker, so the first time you build, it will take time to
pull build the Docker images.  After the initial build, modifying and building
will be much, much faster!

## The Run Script
[run.py](../run.py) is used to handle all tasks. It has only 3 options:

```bash
> ./run.py --help
usage: run.py [-h] [-p PLAYBOOK] [-t TAGS] [-s SERVICES]

optional arguments:
  -h, --help            show this help message and exit
  -p PLAYBOOK, --playbook PLAYBOOK
  -t TAGS, --tag TAGS
  -s SERVICES, --services SERVICES
```
- --playbook: Allows you to specify an Ansible playbook.  If not specified, the
default playbook, [main.yml](../ansible/main.yml) is used. Other playbooks can
be used to shorten the cycle

  - docker_only: use `-p ssl_only` to skip the SSL generation tasks and only
    run the docker tasks.  This is useful after an initial build, if you
    don't need new certs.

  - ssl_only: Just runs the tasks to generate SSL certs.

- --tag: Tags are used to determin which tasks are executed.  The following tags
are currently defined:
  - all: This is the default, and runs all tasks in the playbook.

- --service: Limit execution to the named service. If not provided, all services
will be executed. The services are defined in [conf.d/services.d](../conf.d.services.d/README.md).

