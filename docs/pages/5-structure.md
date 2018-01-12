---
layout: default
title: Specification for the Scientific Filesystem
pdf: true
permalink: /spec
toc: false
---

This document reviews the current specification for the Scientific Filesystem. For the actual specification documents, including older versions, see the [spec folder](https://github.com/vsoch/scif/tree/master/docs/spec) or the [full spec](/scif/specification). As stated in the [introduction](/scif/goals), the scientific filesystem is optimized for provide tools to generate predicible and discoverable scientific containers. The description here describes how to organize software and metadata toward this goal, and encompasses two components:

[Read the Specification Document](/scif/specification)

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
File organization is likely to vary a bit based on the host OS, but arguably most Linux flavor operating systems can said to be similar to the <a href="https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard" target="_blank">Filesystem Hierarchy Standard</a> (FHS). For this discussion, we will disregard the inclusion of package managers, symbolic links, and custom structures, and focus on the core of FHS. We will discuss these locations in the context of how they do (or should) relate to a scientific container. It was an assessment of this current internal standard that led to the original development of SCIF.

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


## SCIF File Organization
The Standard Container Integration Format defines a root base (`/scif`) that can be known and consistently mounted across research clusters. The location was chosen to be independent of any locations on traditional linux filesystems for the sole purpose of avoiding conflicts. Using this namespace, the SCIF has a [set of defaults](/scif/specification#environment-namespace) that are paired with an environment namespace to make it easy to find content. For example, if you were to discover an app named `hello-world` you would have confidence about it's location under `/scif/apps/hello-world` (`$SCIF_APPROOT`).
Along with these locations and environment variables, SCIF is entirely a set of rules about how a container software installs, organizes, and exposes software modules. For the specifics of SCIF we again direct the reader to [the specification](/scif/specification). Here we will wontinue with discussion of its development and rationale, starting with a review of some basic background about Linux Filesystems.


### Apps
Software modules in the context of SCIF are called "apps." and the base of `/scif/apps` is where these apps will live. To read more about apps, [read the Specification Document](/scif/specification).


### Data
The base of `/scif/data` is structured akin to apps - each installed application has its own folder, and additionally a subfolder is created for inputs and outputs:

```
/scif/data
   /foo
      /input
      /output
```

To read more about data, [read the Specification Document](/scif/specification).

<div>
    <a href="/SCI-F/tools.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/SCI-F/examples.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
