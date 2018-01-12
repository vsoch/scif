---
layout: default
title: Example Use Cases
pdf: true
permalink: /examples
toc: true
---

## Example Use Cases
SCI-F is powerful in that it supports multiple general use cases for scientific and systems evaluation and high level introspection. These use cases broadly fall in the areas of providing modular software, systems and metric evaluation, and guided collaboration to answer a scientific question, and are done in context of a Singularity container for maximum reproducibility.

## Quick Examples
You might find SCIF useful if you:

 - want to package multiple environments or software modules in a single container to publish alongside a paper. A scif app might coincide with a particular step in your pipeline, and the entire analysis is run with a few calls to scientific filesystem entrypoints. Bonus points if you package this in a container for reproducibility.
 - you want to provide users with small apps that perform a function (for a host or container) or assess a metric. For example, a scif app installed in a container might serve only to assess different time metrics when the container is building.
 - akin to using a module system, you could use scif to provide different entrypoints for software (coinciding with version, or even the same software with a different environment variable exported to determine runtime behavior.) A good example of this is using common machine learning libraries with different backends (e.g., keras, tensorflow, torch). An entrypoint `keras-python2` would run python with an environment variable triggering using keras as a backend, `keras-python3` would do the same with python3, and then `keras-python` would target the most recent.
 - you want to implement (functionally) the "same thing" in different ways, and assess differences. The simplest example is to imagine recording runtime metrics for a console print of "Hello World" in multiple langauges. Each variation or implementation is a scif app, and the common base is the host or container.


### Modular Software Evaluation
A common question pertains to evaluation of different solutions toward a common goal. An individual might ask "How does implementation **A** compare to implementation **B** as evaluated by one or more metrics?" For a systems admin, the metric might pertain to running times, resource usage, or efficiency. For a researcher, he or she might be interested in looking at variability (or consistency) of outputs. Importantly, it should be possible to give a container serving such a purpose to a third party that does not know locations of executables, or environment variables to load, and the container runs equivalently. SCI-F allows for this by way of providing modular software applications, each corresponding to custom environments, libraries, and potentially files.

#### Method

To demonstrate this use case, we developed a container that implements the most basic function for a program, a print to the console, for each of 19 different languages (*R*, *awk*, *bash*, *c*, *cat*, *chapel*, *clisp*, *cpp*, *csh*, *go*, *julia*, *octave*, *perl*, *python*, *ruby*, *rust*, *tcsh*, *zsh*). The container is designed as a means to collect a series of metrics relative to timing and system resources for each language. The metrics pertain to system resources provided by the <a href="https://linux.die.net/man/1/time" target="_blank">time</a> and <a href="https://linux.die.net/man/1/strace" target="_blank">strace</a> utilities. We will refer to this container generally as "hello-world." A user that did not create the container could ask it for global help:

```
$ singularity help container.img

This container will say hello-world (in dinosaur)!

Examples:

     # See all installed languages
     singularity apps <container>

     # See help for a specific language
     singularity --app <language> <container> help to see help  |or|

     # Run a specific languages
     singularity --app <language> <container>
```

For the "hello-world" container, the output would be as follows: to see all applications installed:

```
$ singularity apps container.img
   awk
   bash
   …
   zsch
```
Or run any particular language:

```
$ singularity run --app bash container.img
RaawwWWWWWRRRR!!
```

Importantly, in the example above, using "run" for the application *bash* handles loading environment variables, adding the application folders to the path, and executing the associated runscript. The application also optionally can serve its own labels, environment metadata, and specifics about its size with the "inspect" command:
singularity inspect --app bash container.img

```
{
    "SINGULARITY_APP_NAME": "bash",
    "SINGULARITY_APP_SIZE": "1MB"
}
```
Therefore, the metric evaluation could be run, across modules, without knowing the applications installed with a simple for loop.

```
for app in $(singularity apps container.img)
    do
    singularity run --app $app container.img
done

```
In the case of metric evaluation, it would be up to the implementor to decide to evaluate the software internally (above) or externally. For example, an external evaluation might look like the following:

```
for app in $(singularity apps container.img)
    do
    /usr/bin/time -a singularity run --app $app container.img
done
```

In practice, for general metrics like timing and host resources, if the container does not provide an app to measure time internally (e.g., an internal app to perform the same call with the "time" executable inside the container), given that the time for Singularity to execute this internal command is trivial or accounted for, it is reasonable to perform tests externally. External tests are advantageous in that containers themselves can be agnostic to the tests - a container does not need to be developed with the internal dependencies to perform any specific test. For tests that look at system calls (e.g., strace as in the example above) calling externally would mean needing to properly account for the call to the singularity software itself in the results.

#### Results

To demonstrate the value of using SCI-F containers, we ran a simple function to print to the command line in 19 languages, and were able to run the analysis in entirety without knowing the specific commands for each language. The resulting table of features pertaining to times (<a href="https://github.com/containers-ftw/hello-world-ftw/blob/master/logs/language-times.tsv" target="_blank"> Supplementary Table 1</a>) and features (<a href="https://github.com/containers-ftw/hello-world-ftw/blob/master/logs/language-features.tsv" target="_blank">Supplementary Table 2</a>) demonstrates a wide span of differences between the seemingly identical calls. For example, Figure 1 shows the differences in "read calls," or the number of read commands to the filesystem issued when the simple "Hello World" command was run: 

<img src="/SCI-F/img/read_calls.png" width="50%"/>

Closer inspection reveals facts about the programs that are common knowledge, such as shell programs having faster start up times than more substantial programs (e.g., *octave*, *R*, or *python*). In fact, the basic differences between start times, reads and writes, and memory usage across this simple execution is surprising, and gives strong support for why scientific results can vary depending on the underlying architecture. It gives even stronger rationale for being able to assess the metadata about the software to reveal cause for the observed differences. Full results and additional analyses are available in <a target="_blank" href="https://github.com/containers-ftw/hello-world-ftw/blob/master/logs/languages_metrics.ipynb">this notebook</a>.

### Modular Metrics Evaluation
For this next use case, a scientist is interested in running a series of metrics over an analysis of interest (the container’s main function, executed by it’s primary runscript).  He has been given a container with a runscript, and several installed supporting metrics (SCI-F apps also in the container), and knows nothing beyond that. 

Each installed SCI-F app can be thought of as a particular context to evoke the container's main runscript, and the apps themselves are relatively agnostic to the runscript itself. Importantly, using the image for its intended purpose is not impacted by the presence of these supporting tools. The command to run the image is unchanged. When the scientist runs the image, he sees it perform it’s primary function, a print of "Hello World!" to the console.

```
$ singularity run metrics.img 
Hello-World!
```

At this point, the scientist doesn’t know what the metrics are, or the particular environment or locations in the container. Given that the container has SCI-F, the scientist can ask the container to tell him what metrics are installed:

```
$ singularity apps metrics.img 
custom
linter
parallel
strace
time
```

And then run the metric easily by simply specifying it’s name:

```
singularity run --app time metrics.img
```

or even writing the previous command into a loop to run all internal apps, without knowing what they are named:

```
for app in $(singularity apps metrics.img)
   do
      singularity run --app $app metrics.img
done
```
This particular container has several metrics to assess usage and timing of different resources (*time*), a complete trace of the call (*strace*), an example custom metric (*custom*), a static linter (*linter*), and a function to run the container’s runscript in parallel (*parallel*). Each of these SCI-F apps serves as an example use case that is discussed in the following sections.

#### Metric Example 1: Evaluate software across different metrics
A system admin or researcher concerned about evaluation of different software
could add relevant metrics apps to the software containers, and then easily evaluate
each one with the equivalent command to the container. Importantly, since each
evaluation metric is a modular app, the container still serves its intended purposes. 
As an example, here is a simple app to return a table of system traces for the
runscript:
```
%apprun strace
    unset SINGULARITY_APPNAME
    exec strace -c -t /.singularity.d/actions/run
```
In the above example, since the main run command for the container looks for the
`SINGULARITY_APPNAME`, we need to unset it first. We then run strace and return
a table that assesses the runscript:

```
 singularity run --app strace metrics.img 
 Hello-World!
 % time     seconds  usecs/call     calls    errors syscall
 ------ ----------- ----------- --------- --------- ----------------
  0.00    0.000000           0        15           read
  0.00    0.000000           0         1           write
  0.00    0.000000           0        35        24 open
  0.00    0.000000           0        17           close
  0.00    0.000000           0        25        12 stat
  0.00    0.000000           0         4           fstat
  0.00    0.000000           0        14           mmap
  0.00    0.000000           0         8           mprotect
  0.00    0.000000           0         2           munmap
  0.00    0.000000           0         6           brk
  0.00    0.000000           0        14           rt_sigaction
  0.00    0.000000           0         6         6 access
  0.00    0.000000           0         2           getpid
  0.00    0.000000           0         2           execve
  0.00    0.000000           0        14           fcntl
  0.00    0.000000           0         2           getdents
  0.00    0.000000           0         3           geteuid
  0.00    0.000000           0         2           getppid
  0.00    0.000000           0         2           arch_prctl
  0.00    0.000000           0         1           openat
  0.00    0.000000           0         1           faccessat
 ------ ----------- ----------- --------- --------- ----------------
 100.00    0.000000                   176        42 total
```

Regardless of what the runscript does, this SCI-F app will provide a consistent way 
to produce this metric. Any user that added the small module to his or her container would immediately have this assessment for the software provided by his or her container. The recipe for this *strace* app is provided at the <a href="http://containers-ftw.org/apps/scif/metrics/bash/metrics-bash-strace/" target="_blank">containers-ftw apps portal</a>, discussed later in this document.


#### Metric Example 2: Custom Functions and Metrics
When a container is intended to only perform one function, this maps nicely to having a single runscript. As the number of possible functions increase, however, the user is forced to either:

 - have a runscript that can take command line options to call different executables
 - use the `exec` command with some known path (to the user)

SCI-F apps allow for an easy way to define custom helper metrics or functions for
the container without needing to write a complicated script or know the locations of executables in a container that was built by another. The app below, also <a href="http://containers-ftw.org/apps/scif/fun/fun-cow-fortune/" target="_blank">provided at the portal</a> is an example of this, as it generates a fortune with a bit of surprise added:

```
singularity run --app custom metrics.img
The difference between the right word and the almost right word is the
difference between lightning and the lightning bug.
		-- Mark Twain
                 (__) 
                 (oo) 
           /------\/ 
          / |    ||   
         *  /\---/\ 
            ~~   ~~   
..."Have you mooed today?"...
```

Although this particular example is comical, the larger idea that individuals can specialize in general modules for assessing containers is a powerful one.


#### Metric Example 3: Code Quality and Linting
A SCI-F app can meet the needs to serve as a linter over a set of files,
or general tests. The example is provided here with a SCI-F app "linter," which runs a linter over a script. 

```
singularity run --app linter metrics.img 

In /scif/apps/linter/lintme.sh line 2:
for f in  do;
^-- SC2034: f appears unused. Verify it or export it.
          ^-- SC1063: You need a line feed or semicolon before the 'do'.
            ^-- SC1059: No semicolons directly after 'do'.


In /scif/apps/linter/lintme.sh line 3:
grep -qi hq.*mp3  && echo -e 'Foo  bar'; done
         ^-- SC2062: Quote the grep pattern so the shell won't interpret it.
                          ^-- SC2039: #!/bin/sh was specified, but echo flags are not standard.
```

This example used a file provided in the container, but a linter app could also accept a command line argument to a file or folder. During building, we advise the researcher to still use the `%test` section to evaluate the outcome of the build process, and to use SCI-F apps for general tests that are generalizable to other containers.


#### Metric Example 4: Runtime Evaluation
In that a metric can call a runscript, it could be easy to evaluate running the main analysis under various levels or conditions. As a simple proof of concept, here we are creating an app to execute the same exact script in parallel.

```
%apprun parallel
    COMMAND="/.singularity.d/actions/run; "
    (printf "%0.s$COMMAND" {1..4}) | parallel

Singularity run --app parallel metrics.img
Hello World!
Hello World!
Hello World!
```

And you might imagine a similar loop to run an analysis, and modify a runtime or system variable for each loop, and save or print the output to the console.

This metrics implementation is available for use at <a href="https://github.com/containers-ftw/metrics-ftw" target="_blank">https://github.com/containers-ftw/metrics-ftw</a> and complete description and documentation at <a href="http://containers-ftw.org/apps/examples/metrics/metrics-ftw" target="_blank">http://containers-ftw.org/apps/examples/metrics/metrics-ftw</a>.

### Contextual Running
It’s often common that a user will want to run a container in different environments, or using different job managers. For example, a scientific analysis run locally would come down to executing the script, but run on a cluster would come down to submission of a job to a SLURM or SGE cluster. In this case, a scientist could distribute the image with easy entry points to each of these use cases:

```
singularity run --app slurm analysis.img
singularity run --app sge analysis.img
```

During the build process, if the resources are available, the researcher can measure metrics like memory needed and time, and then write them into the batch job. Runtime variables like queue and notification email could be provided via variables to the runscript.  This particular example for slurm and sge have been implemented.

 - [SLURM](http://containers-ftw.org/apps/scif/hpc/slurm/hpc-slurm-submit/)
 - [SGE](http://containers-ftw.org/apps/scif/hpc/sge/hpc-sge-submit/)

If a cluster builds and provides containers for the users, the cluster could build the container in each environment, and then provide its own submission script for optimal resource usage.


### Scientific Workflows
The scientist is likely to want to use SCI-F apps for two purposes:

- to provide development containers that expose software to develop pipelines
- to provide a production container alongside a publication to serve a final pipeline 

SCI-F can meet both of these goals, and for this example, we have implemented the equivalent pipeline using Singularity and SCI-F for the CarrierSeq workflow (<a href="https://www.biorxiv.org/content/early/2017/08/18/175281" target="_blank">Mojarro et al. 2017</a>), as well as adding SCI-F to a previously done variant calling analysis that used Singularity and Docker . Each of the two example containers provides modular access to the different software inside. By way of using a Scientific Filesystem (SCI-F), we have a lot of freedom in deciding on what level of functions we want to expose to the user. A developer will want easy access to the core tools (e.g., bwa, seqtk) while a user likely wants one level up, on the level of a collection of steps associated with some task (e.g., mapping).

#### Carrierseq Scientific Pipeline
For this example, we focus on the build recipe that generates a scientific container to perform (optionally) a download of input data, a mapping, statistical (poisson) and sorting procedure. We assume that an interested party has found the container "carrierseq.img", has Singularity installed, and is curious about how to use it. The individual could first ask for help directly from the container.

```
singularity help carrierseq.img

    CarrierSeq is a sequence analysis workflow for low-input nanopore 
    sequencing which employs a genomic carrier.

    Github Contributors: Angel Mojarro (@amojarro), 
                         Srinivasa Aditya Bhattaru (@sbhattaru),   
                         Christopher E. Carr (@CarrCE),
                         Vanessa Sochat (@vsoch).

    fastq-filter from: https://github.com/nanoporetech/fastq-filter
    see:
           singularity run --app readme carrierseq.img | less for more detail

```   
If we follow the instruction, we find the container has an APP that serves only to make the README.md easily accessible:

```
singularity run --app readme carrierseq.img | less

#### CarrierSeq
#### About

bioRxiv doi: https://doi.org/10.1101/175281

CarrierSeq is a sequence analysis workflow for low-input nanopore
            sequencing which employs a genomic carrier.

           Github Contributors: Angel Mojarro (@amojarro), 
                                Srinivasa Aditya Bhattaru (@sbhattaru), 
                                Christopher E. Carr (@CarrCE), 
                                and Vanessa Sochat (@vsoch).
 
fastq-filter from: https://github.com/nanoporetech/fastq-filter

[MORE]
```

Metadata in the way of labels, environment, help, and the runscript and build recipes themselves are available for the whole conatiner in either a json or human readable format via the `--inspect` command:

```
$ singularity inspect carrierseq.img 
{
    "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
    "org.label-schema.usage.singularity.deffile": "Singularity",
    "org.label-schema.usage": "/.singularity.d/runscript.help",
    "org.label-schema.schema-version": "1.0",
    "org.label-schema.usage.singularity.deffile.from": "ubuntu:14.04",
    "org.label-schema.build-date": "2017-09-20T18:16:50-07:00",
    "BIORXIV_DOI": "https://doi.org/10.1101/175281",
    "org.label-schema.usage.singularity.runscript.help": "/.singularity.d/runscript.help",
    "org.label-schema.usage.singularity.version": "2.3.9-development.gaaab272",
    "org.label-schema.build-size": "1419MB"
}
```

And also available on the level of individuals apps:

```
$ singularity inspect --app mapping carrierseq.img
{
    "FQTRIM_VERSION": "v0.9.5",
    "SEQTK_VERSION": "v1.2",
    "BWA_VERSION": "v0.7.15",
    "SINGULARITY_APP_NAME": "mapping",
    "SINGULARITY_APP_SIZE": "9MB"
}
```

All apps are exposed to the user:

```
$ singularity apps carrierseq.img
mapping
poisson
readme
sorting
download
```

And then we can ask for help for any of the pipeline steps:

```
singularity help --app mapping carrierseq.img
singularity help --app poisson carrierseq.img
singularity help --app sorting carrierseq.img
```

The entire set of steps for running the pipeline provided by the container come down to calling the different apps. As an overall strategy, since the data is rather large, we are going to map a folder to the container's data base where the analysis is to run. This directory, just like the modular applications, has a known and predictable location. So our steps are going to look like this:

 0. Download data to a host folder
 1. For subsequent commands, map `/scif/data` to the host folder
 2. Perform mapping step of pipeline
 3. Perform poisson regression on filtered reads
 4. Sort the results

And the calls to the container to support this would be:

```
singularity run --app mapping --bind data:/scif/data carrierseq.img
singularity run --app poisson --bind data:/scif/data carrierseq.img
singularity run --app sorting --bind data:/scif/data carrierseq.img
```

This would be enough to run the pipeline. What do the modules afford us? We can easily isolate metadata and contents related to each step, or shell into the context to test:

```
singularity shell --app mapping carrierseq.img
```

We might also decide that we don't like the "mapping" step, and swap it out for our own:

```
singularity run --app mapping --bind data:/scif/data another-container.img
singularity run --app poisson --bind data:/scif/data carrierseq.img
singularity run --app sorting --bind data:/scif/data carrierseq.img
```

Or a researcher that is incredibly interested in variations of one step (e.g., sorting) could provide an entire container just to serve those variations:

```
singularity run --app quicksort --bind data:/scif/data sorting.img
singularity run --app mergesort --bind data:/scif/data sorting.img
```

Importantly, if we want to understand metadata or container contents relevant to a specific step, this information is represented in the build recipe (provided inside the container), and in the organization of the filesystem itself. We want to reiterate that While the examples above serve different components that might be run by some workflow manager, SCI-F itself is not such an external manager. Rather, SCI-F provides a standard set of commands that would integrate into such a manager. For basic pipelines, and containers that are developed to look for input from the previous step in an expected place, a workflow manager would arguably not needed. While many scientists are comfortable using orchestration of workflows, others are not, and SCI-F works for both cases.

As most workflow components are a carefully chosen set of commands, the container exposes enough metadata to run various steps of the pipeline. The creator of the container has carefully crafted these commands to be specific to his work. For the user, however, knowing the specifics of each command call or path within the container is not so useful for using it. In fact, it might even be a detriment if it confuses the user. This is a very different use case from a scientific developer’s, discussed next.

#### Carrierseq Development Container

The developer has a different use case - to have easy command line access to the lowest level of executables installed in the container. Given a global install of all software, without SCI-F I would need to look at `$PATH` to see what has been added to the path, and then list executables in path locations to find new software installed to, for example, `/usr/bin`. I could only assume that the creator of the container thought ahead to add these important executables to the path at all. Unfortunately, there is no way to easily and programmatically "sniff" a container to understand what changes were made, and what tools are available for development. A container created by developer *Sam* is likely not going to be understood by developer *Stan*.


<img src="/SCI-F/img/robot30.png" width="50%">


The container is a black development box, perhaps only understood by the creator or with careful inspection of the build recipe. We would do well to create a development container with SCI-F, and for this discussion, have created a build recipe that does exactly this.

Still working with CarrierSeq, instead of serving software on the level of the pipeline, we reveal the core software and tools that can be combined in specific ways to produce a pipeline step like "mapping."

```
singularity apps carrierseq.dev.img
bwa
fqtrim
python
seqtk
sra-toolkit
```

Each of the above apps can be used with commands "run", "exec," "inspect," "shell," or "test" to run the container in context of a particular app. This means sourcing app-specific environment variables, and adding executables associated with the app to the path. For example, I can use a simple app "python" to open the python interpreter in the container, or shell into the container to test bwa:

```
##### Open interactive python
singularity run --app python carrierseq.dev.img

##### Load container with bwa on path
$ singularity shell --app bwa carrierseq.dev.img
$ which bwa
$ /scif/apps/bwa/bin/bwa
```

These two images, serving equivalent software, but enabling very different use cases, are good example of the flexibility of SCI-F. 

>> The container creator can choose the level of detail to expose to a user that doesn't know how it was created.

A lab that is using core tools for working with sequence data might have preference for the development container, while a finalized pipeline distributed with a publication would have preference for the first. In both cases, the creator doesn't need to write custom scripts for a container to run a particular app, or to expose environment variables, tests, or labels. 


### Singularity Scientific Example
We adopted an original analysis to compare Singularity vs. Docker on different cloud and local environments  to give rationale for taking a SCI-F apps approach over a traditional Singularity image. We compare the following equivalent (but different!) implementations:

- [Singularity without SCI-F](https://github.com/containers-ftw/scientific-example-ftw/blob/master/Singularity.noscif)
- [Singularity with SCI-F](https://github.com/containers-ftw/scientific-example-ftw/blob/master/Singularity)

The containers use the same software to perform the same functions, but notably, the software and executables are organized differently, and called differently. Singularity standard (the first without SCI-F) relies on external scripts and the container is a bit of a black box. Singularity with SCI-F has no external dependencies beyond data, and is organized according to SCI-F.

The aim here is to qualitatively evaluate SCI-F on its ability to expose container metadata, and information about the pipeline and executables inside. As each evaluation is scoped to the goal's of the container, for this example we focus on the purpose of deploying a set of steps that encompass a pipeline to perform variant calling. For each we will evaluate the container from the perspective of a developer, a user, and a researcher looking to understand software engineering practices using the container.


1. Development Evaluation
For this use case, we are a container developer, and we are writing a singularity build recipe.

Can I easily define multiple entry points?

Standard
Singularity standard defaults to a single runscript per container. If I need to expose multiple functions, I either need to write a more complicated single entrypoint to direct the call, or I need to write detailed docs on different exec commands (and executables inside) for the user to run. For this real world use case, at the time when this runscript was written, SCI-F was not yet conceptualized. Given the sheer number of tools in the container, the runscript served to list a long list of executables, written to a text file, added to the path:


%runscript

    if [ $# -eq 0 ]; then
        echo "\nThe following software is installed in this image:"
        column -t /Software/.info | sort -u --ignore-case        
        echo "\Note that some Anaconda in the list are modules and note executables."
        echo "Example usage: analysis.img [command] [args] [options]"  
    else
        exec "$@"
    fi

Given that this container was intended to run a scientific workflow, this runscript doesn't help to make its usage transparent.  It would be useful for an individual familiar with the core software, perhaps developing a specific workflow with it. Arguably, this complete listing should be provided, perhaps not as a main entrypoint, but a separate app to print metadata, or the software names and versions added as labels to the app(s) where they are relevant. It's important to note that this first container did not include any logic for performing the analysis, this was provided by the included scripts. If the scripts are separated from the container, reproducing the analysis is no longer possible.

SCI-F
SCI-F has the advantage here because I can give names to different apps, and write a different executable runscript for each. I can still provide a main runscript, and it could either give the user a listing of possible options (below) or run the entire workflow the container provides. Here is a main runscript that instructs the user on how to use the apps, dynamically generating the list:

%runscript
 
    if [ $# -eq 0 ]; then
        echo "\nThe following software is installed in this image:"
        ls /scif/apps | sort -u --ignore-case        
        echo "Example usage: singularity --app <name> <container> [command] [args] [options]"  
    else
        exec "$@"
    fi


And here is an example app, specifically to download a component of the data:

%apprun download-reference
    mkdir -p $REF_DIR
    wget -P $REF_DIR ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_25/gencode.v25.transcripts.fa.gz
    gzip -d $REF_DIR/gencode.v25.transcripts.fa.gz
    wget -P $REF_DIR ftp://ftp.ensembl.org/pub/release-85/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
    gzip -d $REF_DIR/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz


Importantly, the scripts that were previously external  are now cleanly organized into sections in the build recipe. This modular organization and easy accessibility would have been very challenging given the first container organization. The runscript would have needed to be long and complicated to infer what the user wanted to do, or the same functionality achieved by executing different scripts (inside the container), which is a non-trivial (or minimally more annoying to write) than simply writing lines into sections.

Can I easily install content known to modules?
Given that I have two functions for my container to perform, foo and bar, can I generate an install routine that will allow for both shared dependencies (i.e. global) and distinct dependencies?

Standard
Singularity standard has one mode to install global dependencies, everything goes into the `%post` script and any organization of required data, files, and libraries is scattered around the image. Other than coming up with a manual organization and documenting it, there is no way to cleanly define boundaries that will be easily discovered by the user. If you take a look at the [Standard Singularity](Singularity.noscif) recipe, you will see this reflected in one huge, single install procedure. As an example, for this container the tools `bwa` and `samtools` were generally used for an alignment step, and there is no way of knowing this. They are installed globally:

```
cd /Software
su -c 'git clone https://github.com/Linuxbrew/brew.git' singularity
su -c '/Software/brew/bin/brew install bsdmainutils parallel util-linux' singularity
su -c '/Software/brew/bin/brew tap homebrew/science' singularity
su -c '/Software/brew/bin/brew install art bwa samtools' singularity
su -c 'rm -r $(/Software/brew/bin/brew --cache)' singularity
``` 

In fact, the `art` tools are installed with the same manager (`brew`), but they belong to an entirely different step. If a research scientist (or user) were parsing this build recipe, or using an NLP algorithm that took distance into account, there would be no strong signal about how these software were used or related to one another.

**SCI-F**
With SCI-F, by simply defining an environment, labels, install, or runscript to be in the context of an app, the modularity is automatically generated. When I add a list of files to an app `foo`, I know they are added to the container's predictable location for `foo`. If I add a file to `bin` I know it goes into foo's bin, and is added to the path when `foo` is run. If I add a library to `lib`, I know it is added to `LD_LIBRARY_PATH` when foo is run. I don't need to worry about equivalently named files under different apps getting mixed up, or being called incorrectly because both are on the path.  For example, in writing these sections, a developer can make it clear that `bwa` and `samtools` are used together for alignment:

```
#### =======================
#### bwa index and align
#### =======================

%appinstall bwa-index-align
    git clone https://github.com/lh3/bwa.git build
    cd build && git checkout v0.7.15 && make
    mv -t ../bin bwa bwakit

    apt-get install -y liblzma-dev
    cd .. && wget https://github.com/samtools/samtools/releases/download/1.5/samtools-1.5.tar.bz2
    tar -xvjf samtools-1.5.tar.bz2
    cd samtools-1.5 && ./configure --prefix=${SINGULARITY_APPROOT}
    make && make install

%apprun bwa-index-align
    mkdir -p $DATADIR/Bam
    bwa index -a bwtsw $DATADIR/Reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa
    bwa mem -t $NUMCORES $DATADIR/Reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa $DATADIR/Fastq/dna_1.fq.gz $DATADIR/Fastq/dna_2.fq.gz | samtools view -bhS - > $DATADIR/Bam/container.bam  

%applabels bwa-index-align
    bwa-version v0.7.15
    samtools-version v1.5
```

and that `art` is used to simulate reads:

```
#### =======================
#### simulate reads
#### =======================

%apphelp simulate-reads
    Optionally set any of the following environment variables (defaults shown)
    READS (100000000)
    READ_LEN (150)
    GENOME_SIZE (3400000000)

%appenv simulate-reads
    READS=${READS:-100000000}
    READ_LEN=${READ_LEN:-150}
    GENOME_SIZE=${GENOME_SIZE:-3400000000}
    export GENOME_SIZE READ_LEN READS

%appinstall simulate-reads   
    wget https://www.niehs.nih.gov/research/resources/assets/docs/artbinmountrainier20160605linux64tgz.tgz
    tar -xzvf artbinmountrainier20160605linux64tgz.tgz 
    mv art_bin_MountRainier/* bin/
    chmod u+x bin/art_*

%apprun simulate-reads
    GENOME="$REF_DIR/Homo_sapiens.GRCh38.dna.primary_assembly.fa"
    FOLD_COVERAGE=$(python -c "print($READS*$READ_LEN/$GENOME_SIZE)")
    art_illumina --rndSeed 1 --in $GENOME --paired --len 75 --fcov $FOLD_COVERAGE --seqSys HS25 --mflen 500 --sdev 20 --noALN --out $FASTQ_DIR/dna_ && gzip $FASTQ_DIR/dna_1.fq && gzip $FASTQ_DIR/dna_2.fq

```

Whether I glanced at the recipe, or did some kind of text processing, I could easily see the relationships and purpose of the software in the container.

#### Can I associate environment and metadata with modules?
Given two different functions for my container to perform, foo and bar, can I define environment variables and labels (metadata) that I know will be sourced (environment) or exposed (inspect labels) in the context of the app?

**Standard**
Singularity standard also has one global shared `%environment`, and `%labels` section. If two functions in the container share the same environment variable and the value is different, this must be resolved manually. For this example, the first container didn't have any labels or environment, however in practice these global sections are usually used for high level, global variables like author and version (of the container). When I run the container, regardless of if different contexts or variables are needed for executables inside, I get the same environment.

**SCI-F**
With SCI-F, I simply write the different variables to their sections, and have confidence that they will be sourced (environment) or inspected (labels) with clear association to the app.

```

%appenv run-rtg
    MEM=${MEM:-4g}
    THREADS=${THREADS:2}
    export MEM THREADS

%applabel run-rtg
    rtg-version 3.6.2
```

#### Do I need to know standard locations in advance?
Given that a container has conformance to SCI-F, do I need to know how it works to use it?

**Standard**
With a standard location, we would be relying on Linux File System conventions (e.g., installation of content to `/usr/local` or intuitively infer that a folder called `/Software` (as with this scientific example) or `/code` is likely where the creator put important content.

**SCI-F**
Instead of requiring the user to know that an app's base might be at `/scif/apps/foo`, we instead expose environment variables (e.g., `SINGULARITY_APPBASE`) that can be referenced at runtime to refer to different apps. This is especially important if, for example, I need to reference the output of one app as input for another, or simply know it's install location. Regardless of which app is running, the container will also expose the top level folder for all apps installations, and data, `SINGULARITY_DATA` and `SINGULARITY_APPS` at `/scif/data` and `/scif/apps`, respectively.


### 2. Production Evaluation
For this use case, we operate under the scenario that we are familiar with Singularity and the commands to use SCi-F, but we know nothing about the containers. We are a user.

#### Do I know what the container does?
The most natural thing to do with a Singularity container, knowing that it is possible to execute, is to do exactly that. For this evaluation, we want to assess how well executing the container reveals the intentions of the creator. 

**Standard**
From the runscript we evaluated earlier, we are presented with a list of software and versions installed in the image, without detail to where or for what purpose. While this listing is comprehensive, it's most appropriate for a developer than a scientific workflow. In this listing, it isn't clear how the software is used or combine in the analysis. We are reliant on some external script or controller that drives the container. We don't have any hints about possible analysis steps the container can serve.

```
The following software is installed in this image:
alabaster           0.7.9     Anaconda
anaconda            4.3.0     Anaconda
anaconda-client     1.6.0     Anaconda
anaconda-navigator  1.4.3     Anaconda
argcomplete         1.0.0     Anaconda
art                 20160605  Homebrew
astroid             1.4.9     Anaconda
astropy             1.3       Anaconda
babel               2.3.4     Anaconda
backports           1.0       Anaconda
beautifulsoup4      4.5.3     Anaconda
bitarray            0.8.1     Anaconda
blaze               0.10.1    Anaconda
bokeh               0.12.4    Anaconda
boto                2.45.0    Anaconda
bottleneck          1.2.0     Anaconda
bsdmainutils        9.0.10    Homebrew
bwa                 0.7.15    Homebrew
cairo               1.14.8    Anaconda
cffi                1.9.1     Anaconda
chardet             2.3.0     Anaconda
chest               0.2.3     Anaconda
click               6.7       Anaconda
cloudpickle         0.2.2     Anaconda
clyent              1.2.2     Anaconda
colorama            0.3.7     Anaconda
conda               4.3.8     Anaconda
conda-build         1.21.3    Anaconda
conda-env           2.6.0     Anaconda
configobj           5.0.6     Anaconda
contextlib2         0.5.4     Anaconda
cryptography        1.7.1     Anaconda
curl                7.52.1    Anaconda
cycler              0.10.0    Anaconda
cython              0.25.2    Anaconda
cytoolz             0.8.2     Anaconda
dask                0.13.0    Anaconda
datashape           0.5.4     Anaconda
dbus                1.10.10   Anaconda
decorator           4.0.11    Anaconda
dill                0.2.5     Anaconda
docutils            0.13.1    Anaconda
dynd-python         0.7.2     Anaconda
entrypoints         0.2.2     Anaconda
et_xmlfile          1.0.1     Anaconda
expat               2.1.0     Anaconda
fastcache           1.0.2     Anaconda
flask               0.12      Anaconda
flask-cors          3.0.2     Anaconda
fontconfig          2.12.1    Anaconda
freetype            2.5.5     Anaconda
get_terminal_size   1.0.0     Anaconda
gevent              1.2.1     Anaconda
glib                2.50.2    Anaconda
greenlet            0.4.11    Anaconda
gsl                 2.3       Homebrew
gst-plugins-base    1.8.0     Anaconda
gstreamer           1.8.0     Anaconda
h5py                2.6.0     Anaconda
harfbuzz            0.9.39    Anaconda
hdf5                1.8.17    Anaconda
heapdict            1.0.0     Anaconda
htslib              1.3.1     Homebrew
icu                 54.1      Anaconda
idna                2.2       Anaconda
imagesize           0.7.1     Anaconda
ipykernel           4.5.2     Anaconda
ipython             5.1.0     Anaconda
ipython_genutils    0.1.0     Anaconda
ipywidgets          5.2.2     Anaconda
isort               4.2.5     Anaconda
itsdangerous        0.24      Anaconda
jbig                2.1       Anaconda
jdcal               1.3       Anaconda
jedi                0.9.0     Anaconda
jinja2              2.9.4     Anaconda
jpeg                9b        Anaconda
jsonschema          2.5.1     Anaconda
jupyter             1.0.0     Anaconda
jupyter_client      4.4.0     Anaconda
jupyter_console     5.0.0     Anaconda
jupyter_core        4.2.1     Anaconda
kallisto            0.43.0    Anaconda
lazy-object-proxy   1.2.2     Anaconda
libbsd              0.8.3     Homebrew
libdynd             0.7.2     Anaconda
libffi              3.2.1     Anaconda
libgcc              4.8.5     Anaconda
libgfortran         3.0.0     Anaconda
libiconv            1.14      Anaconda
libpng              1.6.27    Anaconda
libsodium           1.0.10    Anaconda
libtiff             4.0.6     Anaconda
libxcb              1.12      Anaconda
libxml2             2.9.4     Anaconda
libxslt             1.1.29    Anaconda
_license            1.1       Anaconda
llvmlite            0.15.0    Anaconda
locket              0.2.0     Anaconda
lxml                3.7.2     Anaconda
markupsafe          0.23      Anaconda
matplotlib          2.0.0     Anaconda
mistune             0.7.3     Anaconda
mkl                 2017.0.1  Anaconda
mkl-service         1.1.2     Anaconda
mpmath              0.19      Anaconda
multipledispatch    0.4.9     Anaconda
nb_anacondacloud    1.1.0     Anaconda
nb_conda            1.1.0     Anaconda
nb_conda_kernels    1.0.3     Anaconda
nbconvert           4.2.0     Anaconda
_nb_ext_conf        0.2.0     Anaconda
nbformat            4.2.0     Anaconda
nbpresent           3.0.2     Anaconda
ncurses             6.0_2     Homebrew
networkx            1.11      Anaconda
nltk                3.2.2     Anaconda
nose                1.3.7     Anaconda
notebook            4.3.1     Anaconda
numba               0.30.1    Anaconda
numexpr             2.6.1     Anaconda
numpy               1.11.3    Anaconda
numpydoc            0.6.0     Anaconda
odo                 0.5.0     Anaconda
openpyxl            2.4.1     Anaconda
openssl             1.0.2k    Anaconda
pandas              0.19.2    Anaconda
parallel            20170122  Homebrew
partd               0.3.7     Anaconda
patchelf            0.9_1     Homebrew
patchelf            0.9       Anaconda
pathlib2            2.2.0     Anaconda
path.py             10.0      Anaconda
patsy               0.4.1     Anaconda
pcre                8.39      Anaconda
pep8                1.7.0     Anaconda
pexpect             4.2.1     Anaconda
pickleshare         0.7.4     Anaconda
pillow              4.0.0     Anaconda
pip                 9.0.1     Anaconda
pixman              0.34.0    Anaconda
pkg-config          0.29.1_2  Homebrew
ply                 3.9       Anaconda
prompt_toolkit      1.0.9     Anaconda
psutil              5.0.1     Anaconda
ptyprocess          0.5.1     Anaconda
py                  1.4.32    Anaconda
pyasn1              0.1.9     Anaconda
pycosat             0.6.1     Anaconda
pycparser           2.17      Anaconda
pycrypto            2.6.1     Anaconda
pycurl              7.43.0    Anaconda
pyflakes            1.5.0     Anaconda
pygments            2.1.3     Anaconda
pylint              1.6.4     Anaconda
pyopenssl           16.2.0    Anaconda
pyparsing           2.1.4     Anaconda
pyqt                5.6.0     Anaconda
pytables            3.3.0     Anaconda
pytest              3.0.5     Anaconda
python              3.5.2     Anaconda
python-dateutil     2.6.0     Anaconda
pytz                2016.10   Anaconda
pyyaml              3.12      Anaconda
pyzmq               16.0.2    Anaconda
qt                  5.6.2     Anaconda
qtawesome           0.4.3     Anaconda
qtconsole           4.2.1     Anaconda
qtpy                1.2.1     Anaconda
readline            6.2       Anaconda
redis               3.2.0     Anaconda
redis-py            2.10.5    Anaconda
requests            2.12.4    Anaconda
rope                0.9.4     Anaconda
RTG                 3.6.2     User_Install
ruamel_yaml         0.11.14   Anaconda
samtools            1.3.1     Homebrew
scikit-image        0.12.3    Anaconda
scikit-learn        0.18.1    Anaconda
scipy               0.18.1    Anaconda
seaborn             0.7.1     Anaconda
setuptools          27.2.0    Anaconda
simplegeneric       0.8.1     Anaconda
singledispatch      3.4.0.3   Anaconda
sip                 4.18      Anaconda
six                 1.10.0    Anaconda
snowballstemmer     1.2.1     Anaconda
sockjs-tornado      1.0.3     Anaconda
sphinx              1.5.1     Anaconda
sphinx_rtd_theme    0.1.9     Anaconda
spyder              3.1.2     Anaconda
sqlalchemy          1.1.5     Anaconda
sqlite              3.13.0    Anaconda
statsmodels         0.6.1     Anaconda
sympy               1.0       Anaconda
terminado           0.6       Anaconda
tk                  8.5.18    Anaconda
toolz               0.8.2     Anaconda
tornado             4.4.2     Anaconda
traitlets           4.3.1     Anaconda
unicodecsv          0.14.1    Anaconda
util-linux          2.29      Homebrew
wcwidth             0.1.7     Anaconda
werkzeug            0.11.15   Anaconda
wheel               0.29.0    Anaconda
widgetsnbextension  1.2.6     Anaconda
wrapt               1.10.8    Anaconda
xlrd                1.0.0     Anaconda
xlsxwriter          0.9.6     Anaconda
xlwt                1.2.0     Anaconda
xz                  5.2.2     Anaconda
xz                  5.2.3     Homebrew
yaml                0.1.6     Anaconda
zeromq              4.1.5     Anaconda
zlib                1.2.8     Anaconda
\Note that some Anaconda in the list are modules and note executables.
Example usage: analysis.img [command] [args] [options]
```

**SCI-F**
When we run the SCi-F container, a different kind of information is presented. By listing the container contents at `/scif/apps`, the user knows what pipeline steps are included in the analysis.

```
singularity run scif.img

```

and in fact, this basic listing is generally useful for apps, so it's provided as it's own command, if the user doesn't write a runscript at all:

```
singularity apps scif.img
```

The runscript also hints that I can direct the `%help` command to better understand an app. While both SCiF and standard Singularity allows for specification of a global `%help` section, providing documentation on the level of the application is more focused and offers specificity to the user. Both also allow for global `%labels` that might point to documentation, code repositories, or other informative information.

#### Does moduarity come naturally?
For this metric, we want to know if using different functions of the container (modules) is intuitive. As we have seen above, the definition of a "module" could be anything from a series of script calls to perform a pipeline step (alignment using bwa and samtools), a single script call (such as a module just for bwa), or even the same function applied to a specific set of content (e.g., download "A" v.s. download "B"). 

**Standard**
Singularity proper represents a module on the level of the container. The entire container is intended for one entrypoint, and any deviation from that requires customization of that entrypoint, or special knowledge about other executables in the container to call with `exec`. The container is modular only in context of being a single step in a pipeline.

**SCI-F**
SCI-F, in that the software inside is defined and installed in a modular fashion, makes it easy to find three different modules:

 - download-fastq 
 - download-rtg
 - download-reference

and without looking further, infer that likely these three downloads can be run in parallel. While this doesn't represent any kind of statement or assurance of this, it allows for the container have a natural modularity. Consider steps that are named according to an order:

 - 1-download 
 - 2-preprocess
 - 3-analysis

The creator of the container, in choosing a careful naming, can deliver a huge amount of information about different modules.

#### Do I know what executables are important in the container?
Without much effort, I should have a high level understanding of the different functions that the container performs, as defined by the creator. For example, a container intended for development of variant calling will expose low level tools (e.g, bwa, seqtk) while a container that is intended will expose a pipeline (e.g., mapping).

**Standard**
For Singularity standard, if the container performs one function (and one only), then a single runscript / entrypoint is sufficient. Having multiple functions is completely reliant on the programming ability of the creator. If the creator is able to write a more complex runscript that explains different use cases, the container can satisfy this goal. If not, the container is a black box. 

**SCI-F**
For SCI-F, without any significant programming ability, the different apps are easily exposed to the user.


#### Can I easily get help for an executable?
I should be able to run a command to get help or a summary of what the container does (introspection).

**Standard**
For Singularity standard, you **can** ask a container for help, but it's a single global help.

**SCI-F**
For SCI-F apps, you can define help sections for all of the functions that your container serves, along with a global help.


#### 3. Research Evaluation
An important attribute of having modular software apps is that it allows for separation of files and executables for research, and those that belong to the base system. From a machine learning standpoint, it provides labels for some subset of content in the container that might be used to better understand how different software relates to a pipeline. Minimally, it separates important content from the base, allowing, for example, a recursive tree generated at `/scif` to capture a large majority of additions to the container. Or simple parsing of the build recipe to see what software (possibly outside of this location) was intended for each app. Equally important, having container software installed at a global at `%post` also says important things about it - that it perhaps is important for more than one software module, or is more of a system library.


### Working Environments
SCI-F has a very interesting use case when it comes to working environments. Each app defined in a container can be thought of as running the container under a different context. For example, perhaps a different python base is being used, or a different `LD_LIBRARY_PATH`, or environmet variables exposed for a particular kind of data analysis. To start this discussion, think of all the different ways an app that can be executed can be defined using SCI-F. All of the different options below will result in the same result when running the container in context of an app (e.g., `singularity run --app foo container.img`):

 - A set of commands added to `%apprun`
 - A single file added to the app via `%appfiles`, and then executed in `%apprun`
 - A software module installed with package managers in `%appinstall`, and then executed in `%apprun`

Now we can imagine that the execution of some command is not the goal of the container, but rather providing a particular environment. The  minimum required for an app can be the definition of any section, so we don't need to define a runscript (`%apprun` section) to meet this goal. A container that is intended as a "working container" might simply be a set of `%appenv` sections to define different named environments. Without any other section, the user is then able to interact with the custom, named environments.

```
singularity shell --app tensorflow-gpu container.img
```

### Auditing and Logging
Although we do not delve into this use case, it should be noted that SCI-F apps can provide logging and auditing for containers. A systems administration that builds and provides containers for his or her users might want to enforce running with a standard for logging and auditing. Instead of asking the researcher to write this into his or her custom runscript, the snippet to perform the logging could be added as a SCI-F app dynamically at build time, and then the container run with this context.

<div>
    <a href="/scif/spec"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/scif/community"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>
