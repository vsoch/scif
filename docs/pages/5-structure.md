---
layout: default
title: Specification for the Scientific Filesystem
pdf: true
permalink: /spec
toc: true
---

This document reviews the current specification for the Scientific Filesystem. For the actual specification documents, including older versions, see the [spec folder](https://github.com/vsoch/scif/tree/master/docs/spec) or the [full spec](/scif/specification). As stated in the [introduction](/scif/goals), the scientific filesystem is optimized for provide tools to generate predicible and discoverable scientific containers. The description here describes how to organize software and metadata toward this goal, and encompasses two components:

## 1. Filesystem Structure
[Filesystem structure](#structure) refers to the structure and organization of the filesystem on a host operating system. Importantly, a scientific filesystem must live alongside a standard operating system, but maintain the core of content outside of it. The filesystem can exist in absence of any environment variables or functions to control it, and in that it is organized predictibly, the static folder and file organization has embedded with it knowledge about its usage. We can derive a filesystem structure from a [scif recipe](#recipes) and in turn, we can derive a recipe from a filesystem.

## 2. Environment Variables
The [environment](#environment) is the means by which a scientific filesystem is interacted with. Upon installation or interaction, these variables are defined to drive further operations. For example, when you create a `scif` container, the variables used to generate the filesystem are maintained with the container for subsequent uses. If the user does not have preference, a set of meaningful defaults is used, making general use of scif quick and easy.

## 3. Software and Tools
The Scientific Filesystem provides [software](#software) (a command line utility called `scif`) that can be installed into containers, and then generate and serve as a controller for the entire scientific filesystem when the container is built. See our [examples](/scif/tutorials) for how this works. 

While there are many conventions and tools for organization and control of environments and software, the scientific filesystem is unique in its ease of use and optimized integration with reproducible container technology, and focus on scientific containers.

# Structure
We will start with a review of traditional file organization on a linux machine, and explain the rationale for the organization of SCIF.


## Traditional File Organization
File organization is likely to vary a bit based on the host OS, but arguably most Linux flavor operating systems can said to be similar to the <a href="https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard" target="_blank">Filesystem Hierarchy Standard</a> (FHS). For this discussion, we will disregard the inclusion of package managers, symbolic links, and custom structures, and focus on the core of FHS. We will discuss these locations in the context of how they do (or should) relate to a scientific container. It was an assessment of this current internal standard that led to the original development of SCI-F.

### Do Not Touch
Arguably, the following folders should not be touched by scientific software:

- `/boot`: boot loader, kernel files
- `/bin`: system-wide command binaries (essential for OS)
- `/etc`: host-wide configuration files
- `/lib`: again, system level libraries
- `/root`: root's home. Unless you are using Docker, putting things here leads to trouble.
- `/sbin`: system specific binaries
- `/sys`: system, devices, kernel features

While these locations likely have libraries and functions needed by the host to support software, it should not be the case that a scientist installs his or her software under any of these locations. It would not be easy or intuitive to find or untangle it from what is already provided by the host.

### Variable and Working Locations
The following locations are considered working directories in that they hold variables defined at runtime, or intermediate files that are expected to be purged at some point:

- `/run`: run time variables, should only be used for that, during running of programs.
- `/tmp`: temporary location for users and programs to dump things.
- `/home`: can be considered the user's working space. Singularity mounts by default, so nothing would be valued there. The same is true for..

For example, in the context of a container, it is common practice (at least in the case of Singularity) to mount the user's `/home`. Thus, if a scientist installed his or her software there, the user would not be able to see it unless this default was changed. For these reasons, it is not advisable to assume stability in putting software in these locations.

### Connections
Connections for containers are devices and mount points. A container will arguably always need to be able to support mount points that might be necessary from its host, so it would be important for a scientific container to not put valuables in these locations.

- `/dev`: essential devices
- `/mnt`: temporary mounts.
- `/srv`: is for "site specific data" served by the system. This might be a logical mount for cluster resources.
- `/proc`: connections between processes and resources and hardware information


## SCI-F File Organization
The Standard Container Integration Format defines a root base (`/scif`) that can be known and consistently mounted across research clusters. The location was chosen to be independent of any locations on traditional linux filesystems for the sole purpose of avoiding conflicts. Using this namespace, the SCIF has a [set of defaults](/scif/specification#environment-namespace) that are paired with an environment namespace to make it easy to find content. For example, if you were to discover an app named `hello-world` you would have confidence about it's location under `/scif/apps/hello-world` (`$SCIF_APPROOT`).
Along with these locations and environment variables, SCIF is entirely a set of rules about how a container software installs, organizes, and exposes software modules. For the specifics of SCIF we again direct the reader to [the specification](/scif/specification). Here we will wontinue with discussion of its development and rationale, starting with a review of some basic background about Linux Filesystems.


### Apps
Software modules in the context of SCIF are called "apps." and the base of `/scif/apps` is where these apps will live. We will describe interaction with apps and the file system structure via the implementation in the Singularity software. To allow for this, in the context of Singularity, we provide the following user interface for the developer to install a software module to a container. In the example below, we create a build recipe (a file named Singularity) to start with a base Docker image, ubuntu, and install a hypothetical app "foo" into it from Github:

```
Bootstrap: docker
From: ubuntu:latest

%post
    apt-get update && apt-get -y install foo

%appinstall foo
    git clone ...
    mkdir bin && cd foo-master
    ./configure --prefix=../bin
    make
    make install

%applabels foo
MAINTAINER vsochat@stanford.edu

%appenv foo
FOO=BAR
export FOO

%apptest foo
/bin/bash bin/tests/run_tests.sh

%appfiles foo
README.md README.md 

%apphelp foo

Foo: will produce you bar.
Usage: foo [action] [options] ...
 --name/-n name your bar

%apprun foo

    /bin/bash bin/start.sh
```

In the example above, we defined an application (app) called "foo" and gave the container three sections for it, including a recipe for installation, a simple text print out to show to some user that wants help, and a runscript or entrypoint for the application, with all paths relative to the install folder. The Singularity software would do the following based on this set of instructions:

- Finding the section `%appinstall`, `%apphelp`, `%apprun` is indication of an application command. Not shown but also relevant are `%applabels`, `%appfiles`. and `%apptest`.
- The following string (e.g. `foo`) is parsed as the name of the application, and a folder is created, in lowercase, under `/scif/apps` if it doesn't exist.  A singularity metadata folder, `scif`, with equivalent structure to the container’s main metadata folder (`/.singularity.d`), is generated inside the application. An application thus is like a smaller image inside of it’s parent.
- A "bin" folder is automatically genereated for `foo`, and will be automatically added to `$PATH` when `foo` is being used. A "lib" folder is also generated, and is added to `$LD_LIBRARY_PATH` when `foo` is used.
- Based on the section name (e.g. "run"), the appropriate action is taken:
  - `%appinstall` corresponds to executing commands within the folder to install the 
application. These commands would previously belong in %post, but are now attributable 
to the application.
  - `%apphelp` is written as a file called runscript.help in the application's metadata folder, 
where the Singularity software knows where to find it. If no help section is provided, the 
software simply will alert the user and show the files provided for inspection.
  - `%apprun` is also written as a file called runscript.exec in the application's metadata 
folder, and again looked for when the user asks to run the software. If not found, the container should default to shelling into that location.
  - `%applabels` will write a labels.json in the application's metadata 
folder, allowing for application specific labels. 
  - `%appenv` will write an environment file in the application's base folder, allowing for definition of application specific environment variables. 
  - `%apptest` will run tests specific to the application, with present working directory assumed to be the software module’s folder


### Data
The base of `/scif/data` is structured akin to apps - each installed application has its own folder, and additionally a subfolder is created for inputs and outputs:

```
/scif/data
   /foo
      /input
      /output
```

SCI-F does not enforce or state how the container creator should use the data folders, but rather encourages the creator to use the organization so that a user can intutiively know that any input for app `foo` might go into `/scif/data/foo/input`, general data for `foo` might be in `/scif/data/foo`, and global data for the entire container might be in `/scif/data`. For example, <a href="http://containers-ftw.org/apps/examples/carrierseq" target="_blank">this scientific workflow</a> mounts a host folder at `/scif/data`, and then each application creates it's needed data folders at runtime simply by referencing an environment variable specific to the app. For intermediate data, the user could use a mounted data folder, or use a temporary or working directory. As container functions and integrations are further developed, we expect this simple connection into a container for inputs and outputs specific to an application to be very useful. As for the organization and format of the data for any specific application, this is up to the application. Data can either be included with the container, mounted at runtime from the host filesystem, or connected to what can be considered a "data container."

Akin to software modules, overlap in data modules is not allowed by way of the unique app names afforded by folders under a common directory. For example, let's say we have an application called "foo".

- users and developers would know that foo's data would be mounted or provided at `/scif/data/foo`. The directory is guaranteed to exist in the container, and this addresses the issue of some clusters not being able to generate directories in the container that don't exist at runtime.
- importing of datasets that follow some other specific format would be allowed, eg `/scif/data/foo/bar1` and `/sci/data/foo/bar2`.

An application's data would be traceable to the application by way of it's identifier. Thus, if I find `/scif/data/foo` I would expect to find related software under `/scif/apps/foo`.


# Environment

Runtime Environment

When we run the container in context of an app, we see that the running app (top section of variables) reveals a global/general variable to indicate the active app, and the others are still available (for apps to communicate with one another). Note that I re-ordered this list to show this distinction.

 singularity exec --app hub sregistry.simg env | grep SCIF

# Here are variables for active app (hub)
SCIF_APPDATA=/scif/data/hub
SCIF_APPROOT=/scif/apps/hub
SCIF_APPNAME=hub
SCIF_APPMETA=/scif/apps/hub/scif

# These refer to SCIF, globally
SCIF_DATA=/scif/data
SCIF_APPS=/scif/apps

# And specific for all apps, for internal reference
SCIF_APPDATA_google_drive=/scif/data/google-drive
SCIF_APPRUN_google_drive=/scif/apps/google-drive/scif/runscript
SCIF_APPROOT_google_drive=/scif/apps/google-drive
SCIF_APPLIB_google_drive=/scif/apps/google-drive/lib
SCIF_APPMETA_google_drive=/scif/apps/google-drive/scif
SCIF_APPBIN_google_drive=/scif/apps/google-drive/bin
SCIF_APPENV_google_drive=/scif/apps/google-drive/scif/env/90-environment.sh
SCIF_APPLABELS_google_drive=/scif/apps/google-drive/scif/labels.json

SCIF_APPLABELS_registry=/scif/apps/registry/scif/labels.json
SCIF_APPDATA_registry=/scif/data/registry
SCIF_APPRUN_registry=/scif/apps/registry/scif/runscript
SCIF_APPROOT_registry=/scif/apps/registry
SCIF_APPLIB_registry=/scif/apps/registry/lib
SCIF_APPMETA_registry=/scif/apps/registry/scif
SCIF_APPBIN_registry=/scif/apps/registry/bin
SCIF_APPENV_registry=/scif/apps/registry/scif/env/90-environment.sh

SCIF_APPENV_google_storage=/scif/apps/google-storage/scif/env/90-environment.sh
SCIF_APPLABELS_google_storage=/scif/apps/google-storage/scif/labels.json
SCIF_APPDATA_google_storage=/scif/data/google-storage
SCIF_APPRUN_google_storage=/scif/apps/google-storage/scif/runscript
SCIF_APPROOT_google_storage=/scif/apps/google-storage
SCIF_APPLIB_google_storage=/scif/apps/google-storage/lib
SCIF_APPMETA_google_storage=/scif/apps/google-storage/scif
SCIF_APPBIN_google_storage=/scif/apps/google-storage/bin

SCIF_APPENV_hub=/scif/apps/hub/scif/env/90-environment.sh
SCIF_APPLABELS_hub=/scif/apps/hub/scif/labels.json
SCIF_APPDATA_hub=/scif/data/hub
SCIF_APPRUN_hub=/scif/apps/hub/scif/runscript
SCIF_APPROOT_hub=/scif/apps/hub
SCIF_APPLIB_hub=/scif/apps/hub/lib
SCIF_APPMETA_hub=/scif/apps/hub/scif
SCIF_APPBIN_hub=/scif/apps/hub/bin



### Environment Variables
Discovery of data and app folders is helped by way of environment variables. When the container is run in context of an app:

```
singularity run --app foo container.img
```

a set of environment variables about locations for the app's data and executables are exposed. Variables are also exposed for these locations for other apps, and both these sets of variables makes it easy for the creator and user to reference locations without knowing the actual paths. Thus, a container with SCI-F apps provides the following (automatically generated) runtime environment variables that can be used in build recipes over hard coded paths. Given the implementation in Singularity containers, these variables are prefixed appropriately:

 - `SINGULARITY_APPS`: An environment variable to point to the global apps base, `/scif/apps`
 - `SINGULARITY_DATA`: points to the global data base, `/scif/data`
 - `SINGULARITY_APPDATA`: references the app that is being run (e.g., `foo`), pointing to an app's data base (`/scif/data/foo`)
   - `SINGULARITY_APPINPUT`: references inputs (`/scif/data/foo/input`)
   - `SINGULARITY_APPOUTPUT`: references output (`/scif/data/foo/input`)

The next set of variables are defined for every app, regardless of the current running. This makes it possible to know the path to another app's data (e.g.. `bar`) while running `foo`):

 - `APPROOT_<bar>`: defined as (`/scif/apps/bar`)
 - `APPDATA_<bar>`: defined as (`/scif/data/bar`)

While SCi-F is not a workflow manager, it follows naturally that the creator of a SCI-F app might use these internal variables to have modules internally talk to one another. The user and creator do not need to know the structural specifics of the standard, but only how to reference them.

### Interaction
A powerful feature of container software applications is allowing for programmatic accessibility to a specific application within a container. For each of the Singularity software’s main commands, run, exec, shell, inspect and test, the same commands can be easily run for an application. 


#### Listing Applications
If I wanted to see all applications provided by a container, I could use singularity apps:

```
singularity apps container.img
bar
foo
```

#### Application Run
To run a specific application, I can use run with the --app flag:

```
singularity run --app foo container.img
RUNNING FOO
```

This ability to run an application means that the application has its own runscript, defined in the build recipe with `%apprun foo`. In the case that an application doesn’t have a runscript, the default action is taken, shelling into the container:

```
Singularity run --app bar container.img
No Singularity runscript found, executing /bin/sh
Singularity> 
```


#### Application Execution and Testing

For the commands shell and exec, in addition to the base container environment being sourced, if the user specifies a specific application, any variables specified for the application’s custom environment are also sourced.

```
     singularity shell --app foo container.img
     singularity exec --app foo container.img
```

Note that unlike a traditional shell command, we are shelling into the container with the environment and relevant context for `bar` activate. Running the command makes the assumption the user wants to interact with this software. An application with tests can be also be tested:

```
singularity test --app bar container.img
```


#### Application Inspect and Help
In the case that a user wants to inspect a particular application for a runscript, test, or labels, that is possible on the level of the application:

```
singularity inspect --app foo container.img
{
    "SINGULARITY_APP_SIZE": "1MB",
    "SINGULARITY_APP_NAME": "foo",
    "HELLOTHISIS": "foo"
}
```

The above shows the default output, the labels specific to the application foo. The user can also ask for a snippet of help text for a single app:

```
singularity help --app foo container.img
Foo: will produce you bar.
Usage: foo [action] [options] ...
 --name/-n name your bar

```


### Metadata
A software or data module, in its sparsest state, is a folder of files with a name that the container points the user to. However, given easy development and definition of modules, SCI-F advocates for each application having a minimal amount of metadata. For standardization of labels, Singularity containers follow the org.label-schema specification, for which we aim to add a simple set of labels for scientific containers

- org.label-schema.schema-version: is in reference to the schema version.
- org.label-schema.version: in addition to a unique identifier provided by the folder name, a version number provided as a label or with running the software with --version
- org.label-schema.hash-md5sum: a content hash of it's guts (without a timestamp), which could easily be provided by Singularity at bootstrap time
- org.label-schema.build-date: the date when the container was generated, or the software module was added.

The metadata about dependencies and steps to create the software would be represented in the `%appinstall`, which is by default saved with each container. Metadata about different environment variables would go into `%appenv`, and labels that should be accessible statically go into `%applabels`. Help for the user is provided under `%apphelp`.


<div>
    <a href="/SCI-F/tools.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/SCI-F/examples.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
