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

## Create a Python Virtual Environment and install Python packages
The preferred way to manage python projects is to use Python VirtualEnv.  This
creates an isolated Python environment, seperate from your system environent.
The `install.sh` script in the fapi-demo root folder should do everything.

Run the python setup as follows:
```bash
> ./install.sh
```
Once complete, and anytime you create a new terminal window, you need to run the following, to
activate the Python VirtualEnv:
```bash
> . ./venv/bin/activate
```
