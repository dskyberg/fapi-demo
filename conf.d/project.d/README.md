# Project Configuration
The project configuration has two sections:

## Project configuration

[00.conf.yml](00.conf.yml) contains the following values:
- rootDir: Set to the top level folder.  You need to set this
buildDir: The name of the director under the rootDir for output
dockerDir: The directory under rootDir that contains the Docker contexts for builds.
timezone: The default timezone for each container.

## Product and lib versions
[01.versions.yml](01.versions.yml) contains the versions of various libraries,
and Docker images used.  This makes it a bit easier to specify version info
for Dockerfiles.  Currently, Node, Yarn, Postgres, and PingFederate are specified.