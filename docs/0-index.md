---
layout: default
title: {{ site.name }}
pdf: true
permalink: /
---

<div style="float:right; margin-bottom:50px; color:#666">
Version: {{ site.version }}<br>
Date: 2017-xx-xx
</div>

<div>
    <img src="img/logo/scif-slash-green.png" width="300px" style="float:left">
    <h1 style="margin-top:10px">Scientific Filesystem</h1>
</div><br><br>

Here we present the Scientific Filesystem (scif), an organizational format that supports exposure of executables and metadata for discoverability. The format includes a known *filesystem structure*, a definition for a set of *environment variables* describing it, and *functions* for generation of the variables and interaction with the libraries, metadata, and executables located within. [*[quick start](/scif/tutorial-quick-start)*] or [*[really quick start](/scif/tutorial-really-quick-start)*].

## How does scif related to containers?
Although scif is not exclusively for containers, in that a container can provide an encapsulated, reproducible environment, the scientific filesystem works optimally when contained. Containers traditionally have one entrypoint, one environment context, and one set of labels to describe it. A container created with a Scientific Filesystem can expose *multiple* entry points, each that includes its own environment, metadata, installation steps, tests, files, and a primary executable script. SCIF thus brings internal modularity and programatic accessibility to encapsulated, reproducible environments.


## What will I learn reading this?
We will start by reviewing the background and rationale for a scientific organizational format, and how SCI-F achieves the goals of **modularity**, **transparency**, and **consistency**. We then review the organizational structure of the standard, and the different levels of internal modules that it affords. For this work, we provide several tutorials to demonstrate using the scientific filesystem with Docker and Singularity, and additionally have implemented and released the organizational format as a native integration with the Singularity software. Finally, we discuss use cases for SCI-F in context of containers, including how scif can be used to evaluate software, provide metrics, serve scientific workflows, and execute a primary function under different contexts. To encourage collaboration and sharing of apps, we have developed an open source, version controlled, tested, and programmatically accessible web infrastructure at <a href="http://containers-ftw.org/apps" target="_blank">http://containers-ftw.org/apps</a>. For developers, we provide a getting started guide for integration of SCI-F into other container technologies or contexts. The ease of using SCI-F to develop scientific containers offers promise for scientists to easily generate self-documenting containers that are programmatically parseable, exposing software and associated metadata, environments, and files to be quickly found and used. 


### Getting Started

 - [Tutorils](/scif/tutorials): are a good place to start if you are a user or developer. These pages will show you how you generate and interact with a scientific filesystem. Or jump right in to a *[quick start](/scif/tutorial-quick-start)* or *[really quick start](/scif/tutorial-really-quick-start)*.
 - [Goals](/scif/goals): here we review how SCI-F allows for internal modularity and consistency, transparency, and reproducible practices.
 - [Examples](/scif/examples): Whether you are a system admin, a developer, or a research scientist, why would you want to use SCI-F anyway?
 - [Specification](/scif/spec): reviews the current specification for SCI-F.

### Resources

 - [Community](/scif/community): community resources including APIs, version control and testing, and open source forums for tracking issues and discussion related to SCI-F and scientific filesystem apps.


We have provided several <a href="http://containers-ftw.github.io/apps/category/#Example" target="_blank">examples and tutorials</a> for getting started with SCI-F. If you have a workflow or container that you'd like to see added, please <a href="https://www.github.com/containers-ftw/apps/issues" target="_blank">reach out</a>. If you would like to see other ways to contribute, <a href="/SCI-F/community.html#contribute-to-sci-f">here are some suggestions</a>. This work will remain open for contributions, and early contributions will be represented in an official submission.

<div>
    <a href="/scif/intro.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
