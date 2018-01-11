---
layout: default
title: Scientific Filesystem Goals
pdf: true
permalink: /goals
toc: true
---

# Philosophy
The philosophy behind the scientific filesystem is that we are empowered to better use software when clear entrypoints are defined, predictible, and discoverable.

 1. discoverability means that we have knowledge that software exists
 2. predictibility is a means to interact with software without having prior knowledge to its creation

At it's core, the scientific filesystem is a simple [description](/scif/spec) of how to organize software and metadata on a filesystem for discoverability. This description encompasses a **filesystem structure** to ensure that scientific software is distinct from standard software on the host, and is interacted with by way of a set of **environment variables** and **functions** to expose the structure to the user. In that containers provide encapsulated, reproducible environments, SCIF works optimally when installed and used within a container. With SCIF you can:

 1. write **recipes** that define environments, metadata, executables, and dependencies for a grouping of scientific software
 2. **install** the recipe into a container
 3. programatically and easily interact with the scientific software
 4. share your containers or recipes with confidence of discoverability

A container that is found to have a SCIF filesystem, without any additional definition, has a known method of interaction without any special knowledge. We will discuss this in more detail in the following sections.

## What SCIF is not:
SCIF handles the step that comes before any kind of workflow manager is used, and is best used alongside some kind of container technology. It works with, and does not replace either of those things.

**a workflow manager**
The scientific filesystem does not handle the details of connecting inputs and outputs, or typical functions we associate with workflow managers. SCIF, in that it gives structure to executables and content for these managers, adds to this ecosystem, but is agnostic to the particulars of user interaction with any particular software.

**a dependency manager**
SCIF is agnostic to where you are using it. For reproducible software modules, especially those that require dependencies on top of the system, it is strongly recommended to use a container technology, and we provide numerous [tutorials and examples](/scif/tutorials) for doing this. For those that have preference for working without a container, SCIF works just as easily on a host machine as it does a Docker or Singularity container, and in fact, many of the same functions can be run in a preview mode to assess functionality.


## Goals

For the official description of goals, see [the specification](/scif/specification#goals). In the following sections, we hope to show that SCIF is useful because it allows for:

 - [flexible, internal modularity](#modules) where the definition of modularity is entirely based on the needs of the creator and user, and the resulting container reflects that.
 - [reproducible practices](#reproducible-practices) by way of providing portable environments with modular internal contents that are easily discovered.


While SCi-F is not a workflow manager, it follows naturally that the creator of a SCIF app might use these internal variables to have modules internally talk to one another. The user and creator do not need to know the structural specifics of the standard, but only how to reference them.

# Modules

Modularity can be understood as the level of dimensionality that a user is instructed to operate, and for the purposes of this discussion we will suggest three general levels. 

 - **Node** For those familiar with container technology, it is commonly the case that an entire container is considered a module. An example is a container that performs the task of variant calling. If the container itself is considered the module, the user would expect to provide raw data inputs, and receive final results as an output. The container acts as a node that plugs into higher level orchestration tools. The node representation is ideal if the container is expected to plug into a workflow manager and perform one task.
 - **Internal**: A second common scenario might be a single container that holds executables to perform different steps of a pipeline, perhaps so that the researcher can use the same container to run multiple steps, or perform any number of steps in parallel. This container would come with multiple *internal modules*, each performing a series of commands for one step in the pipeline (e.g., the step "mapping" uses internal commands from software `bwa` and `samtools`). The user doesn't need to know the specifics of the steps, but how to call them. We call this level "internal modules" because without any formal structure for the contents of containers, they are hidden, internal executables that must be found or described manually.
 - **Development**: Containers can also serve modules that are represented at the ideal level for development. For this example, instead of providing the container as a node, or actions inside like "mapping", the smallest units of software are exposed, such as the executables `bwa` and `samtools`. It would be likely that a researcher developing a scientific pipeline would find this useful.

Given the different needs briefly explained above, it is clear that there is no correct level of dimensionality to define a module. 

>> The definition of modularity is entirely based on the needs of the creator and user. 

If we discover a container after creation, it cannot be clear without suitable documentation what level is represented, or how to interact with the container. What is needed is an ability for the creator of a container to implicitly define this level of usage simply by way of creating the container. SCIF allows us to do this. We can define modules on the levels of single files, or groups of software to perform a task. The metadata and organization of our preferences is automatically generated to create a complete, and programmatically understandable software package or scientific analysis.


# Reproducible Practices
We have just discussed why internal modularity is important for container interaction, and this is also the case that it's useful for reproducibility. It is important to distinguish the entire container as a reproducible product, and different software modules inside of it that depend on being served through the container to ensure reproducibility. While the container itself is portable, and designed to contain all dependencies to support reproducibility, the SCi-F module in and of itself is not guaranteed to be. For example, a user might define a  module only with an `%apprun` section, implying that the folder only contains a runscript to execute. The user may have chosen to install dependencies for this script globally in the container, in the `%post` section, because perhaps they are shared across multiple modules. Under these conditions, if another user expected to add the module to a different build recipe, the dependencies from `%post` would be needed too. The host operating system also needs to be taken into consideration. A module with dependencies installed from the package manager "yum" would not move seamlessly into a debian base. However, appropriate checks and balances can be implemented into the process of moving applications:

 - For applications that must be portable outside of their initial container, users would be encouraged to include all dependency installs within the `%appinstall` section. If they were already installed during `%post`, the package would be found and skipped.
 - Installing an application into a container would check for OS compatibility. This can be done automatically by storing information about the base OS with each application as a label. To encourage this practice, we have added a test and requirements of specifying one or more operating systems for any module contributed at <a href="https://containers-ftw.github.io/apps" target="_blank">https://containers-ftw.github.io/apps</a>. With these checks, we can have some confidence that the recipes for generating the apps are maximally portable.

Modular internal contents combined with reproducible portable environments via Singularity containers is a starting point for practicing good science.


<br>
<div>
    <a href="/scif/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/scif/tools.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
