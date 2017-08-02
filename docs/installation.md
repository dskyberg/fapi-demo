# Installing the system

## Install Dependencies

### 1. Python
Python3 is required.

### 1. Docker
This demo requires docker to be installed.  If you are running on linux, just
use your standard install utility to install Docker.  Ie, for Ubuntu:

```bash
> sudo apt-get update && apt-get install docker && apt-get clean
```
If you are running on Windows, follow [Install Docker for Windows](https://docs.docker.com/docker-for-windows/install/) to install the latest stable [InstallDocker.msi](https://download.docker.com/win/stable/InstallDocker.msi).

If you are running on Mac OS X, follow [Install Docker for Mac](https://docs.docker.com/docker-for-mac/install/) to install the latest stable [Docker.dmg](https://download.docker.com/mac/stable/Docker.dmg)


## Check out the repo
```bash
git clone https://www.github.com/dskyberg/fapi-demo
```

## [OPTIONAL] Create a Python Virtual Environment
The preferred way to manage python projects is to use
[Python VirtualEnv](https://virtualenv.pypa.io/en/stable/).  This
creates an isolated Python environment, seperate from your system environent. If
you don't already have virtualenv, run the following:

```bash
$ [sudo] pip install virtualenv
```
You can now create a local python environment by running:

```bash
$ usr/bin/env python3 /usr/local/lib/python3.5/site-packages/virtualenv.py venv
```
activate the Python VirtualEnv:
```bash
$ . ./venv/bin/activate
```

You will need to repeat this command once in any new terminal window that you want
to run the python libs from.

## Install the python dependencies
The file `<fapi-demo>/scripts/install_python_libs.sh` has a listing of all the
dependency libs necessary for the demo, including the Ansible libs.  Just run it:

```bash
$ ./scripts/install_python_libs.sh
```
Once complete, and anytime you create a new terminal window, you need to run the following, to
