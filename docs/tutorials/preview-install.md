---
layout: default
title: Preview and Install the Scientific Filesystem
pdf: true
permalink: /tutorial-preview-install
toc: false
---

Here we will start with a scientific filesystem recipe, preview what it produces, and then install a scientific filesystem. This is likely the most common use case, and we will do the following:

 0. **Create** a SCIF recipe
 1. **Preview** recipe install on the host
 2. **Install** SCIF in container (Docker or Singularity) using Recipe
 3. **Export** or reverse engineer recipe from SCIF

In the above, you will see that we will go full circle! Using SCIF, we are able to start with a text description of a set of applications (the recipe), produce a SCIF, and then reverse engineer the recipe from the SCIF.

```
+--------------------+        +--------------------+       +--------------------+
|                    |        |                    |       |                    |
|                    |        |                    |       |                    |
|                    |        |                    |       |                    |
|                    |        |                    |       |                    |
|       Recipe       +-------->      Preview       +------->     Scientific     |
|                    |        |         then       |       |     Filesystem     |
|                    |        |      Install       |       |                    |
|                    |        |                    |       |                    |
|                    |        |                    |       |                    |
+----------^---------+        +--------------------+       +----------+---------+
           |                                                          |
           |                                                          |
           |                                                          |
           +----------------------------------------------------------+
```

and once we have a SCIF, even if we don't have the knowledge of the creator that wrote its recipe, because it exposes commands and metadata for discoverability, we can easily, programmatically interact with it without knowing the details:

```
+--------------------+  +-------------+
|                    +-->  Run        |
|                    |  +-------------+
|                    |  +-------------+
|                    +-->  Inspect    |
|     Scientific     |  +-------------+
|     Filesystem     |  +-------------+
|                    +-->  Shell      |
|                    |  +-------------+
|                    |  +-------------+
|                    +--> Exec        |
+--------------------+  +-------------+
```

You will recognize many of these functions map to those you are familiar with for interacting with containers, and in some respect they will feel very similar. The difference is that we are interacting directly with the SCIF in the container. If you installed the SCIF in another container (perhaps with an different external interface for interaction) you could have confidence that given that the container has SCIF installed at the entrypoint, your interaction will not be very different. We will discuss this more later in the next tutorial to [run SCIF](tutorial-run.md). For now, let's take a look at writing, previewing, and installing a recipe to generate a SCIF.


## Writing a SCIF recipe
Let's first write a recipe, a text file called [hello-world.scif](hello-world.scif), to produce different variations of hello world (with an echo, and with executing of a script).

```
%appenv hello-world-echo
    THEBESTAPP=$SCIF_APPNAME
    export THEBESTAPP
%apprun hello-world-echo
    echo "The best app is $THEBESTAPP"

%appinstall hello-world-script
    echo "echo 'Hello World!'" >> bin/hello-world.sh
    chmod u+x bin/hello-world.sh
%appenv hello-world-script
    THEBESTAPP=$SCIF_APPNAME
    export THEBESTAPP
%apprun hello-world-script
    /bin/bash hello-world.sh
```

Notice that I'm using three sections, 

 - `appinstall` for any install routine particular for the app
 - `apprun` for the entrypoint to the app. This could be executing of a script, or a general command. 
 - `appenv`  for any environment variables speific to the app.

and you might not even need that many! An app can just be an environment, for example, or a single command to run. If you are interested in the different sections allowed for the specification, or the many flexible ways to generate an app, read our [recipes guide](/scif/recipes) to learn more.


## Preview the recipe
I next would want to preview the recipe. What changes would be made on a host, and where? I feel comfortable doing this on my host because it isn't actually going to make any changes. After I have installed `scif` (`pip install scif`) I can do this from the command line:

```
[base] /scif 
[apps] /scif/apps 
[data] /scif/data
 

[root] /scif/apps/hello-world-echo 
[lib] /scif/apps/hello-world-echo/lib 
[bin] /scif/apps/hello-world-echo/bin 
[data] /scif/data/hello-world-echo 
+ apprun hello-world-echo
/scif/apps/hello-world-echo/scif/runscript
/scif/apps/hello-world-echo/scif/runscript.help
echo "The best app is $THEBESTAPP"
+ appenv hello-world-echo
/scif/apps/hello-world-echo/scif/environment.sh
THEBESTAPP $SCIF_APPNAME
+ apprecipe hello-world-echo
/scif/apps/hello-world-echo/scif/hello-world-echo.scif


[root] /scif/apps/hello-world-script 
[lib] /scif/apps/hello-world-script/lib 
[bin] /scif/apps/hello-world-script/bin 
[data] /scif/data/hello-world-script 
+ apprun hello-world-script
/scif/apps/hello-world-script/scif/runscript
/scif/apps/hello-world-script/scif/runscript.help
/bin/bash hello-world.sh
+ appenv hello-world-script
/scif/apps/hello-world-script/scif/environment.sh
THEBESTAPP $SCIF_APPNAME
+ appinstall hello-world-script
echo "echo 'Hello World!'" >> $SCIF_APPBIN/hello-world.sh
chmod u+x $SCIF_APPBIN/hello-world.sh
+ apprecipe hello-world-script
/scif/apps/hello-world-script/scif/hello-world-script.scif
```

It's pretty straight forward - each section pertains to an app, and first shows the root, lib, bin, and data folders for the app, and then the files that will be produced on install. The very top section shows the global changes (e.g., the global scif folders for data and apps. I can also run this command 
to just preview one app from the recipe:

```
$ scif preview hello-world.scif hello-world-echo
[base] /scif 
[apps] /scif/apps 
[data] /scif/data
 

[root] /scif/apps/hello-world-echo 
[lib] /scif/apps/hello-world-echo/lib 
[bin] /scif/apps/hello-world-echo/bin 
[data] /scif/data/hello-world-echo 
+ apprun hello-world-echo
/scif/apps/hello-world-echo/scif/runscript
/scif/apps/hello-world-echo/scif/runscript.help
echo "The best app is $THEBESTAPP"
+ appenv hello-world-echo
/scif/apps/hello-world-echo/scif/environment.sh
THEBESTAPP $SCIF_APPNAME
+ apprecipe hello-world-echo
/scif/apps/hello-world-echo/scif/hello-world-echo.scif
```

If you choose an app that doesn't exist, it will tell you that.

```
[base] /scif 
[apps] /scif/apps 
[data] /scif/data
 
ERROR Cannot find app hello-world in config.
```

We can also do this interactively! scif comes with a development shell command, `pyshell`, that will either let you interact with a recipe, **or** a filesystem. The general command works as follows:


#### SCIF Python (pyshell) Options

|  example            | use case                                | 
|---------------------|-------------------------------------------|
| scif pyshell [recipe] | interact with a recipe, no changes to the filesystem (akin to preview) |
| scif pyshell          | interact with a SCIF (no SCIF app active) |
| scif pyshell [app]    | interact with a SCIF with an app active.  |
| scif pyshell [recipe] [app]    | interact with a recipe, still no changes, but load context of an app|


There also is a `shell` command for the equivalent interaction, however we would need to install a SCIF first:

```
scif shell
WARNING /scif is not detected as a recipe or base.
```

Well let's install it then! But first, let's interactively explore the recipe, `hello-world.scif` with the python shell (pyshell)

```
$ scif pyshell hello-world.scif
[scif] /scif hello-world-echo | hello-world-script
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: 
```

We can look at the ScifRecipe object, and then client instantiated from it:

```
In [1]: ScifRecipe
Out[1]: scif.main.base.ScifRecipe

In [2]: client
Out[2]: [scif]
```

and then produce the same output from the preview above (the recipe is already loaded, so we don't need to supply it)

```
client.preview()
```

We can list all apps

```
In [4]: client.apps()
Out[4]: ['hello-world-echo', 'hello-world-script']
```

or look at the specifics for a particular app:

```
In [5]: client.app('hello-world-script')
Out[5]: 
OrderedDict([('appinstall',
              ['echo "echo \'Hello World!\'" >> $SCIF_APPBIN/hello-world.sh',
               'chmod u+x $SCIF_APPBIN/hello-world.sh']),
             ('appenv', ['THEBESTAPP $SCIF_APPNAME']),
             ('apprun', ['/bin/bash hello-world.sh'])])
```

Notice that we have an ordered dict, and the reason is so that the app lookup respects the order that you write the sections in the recipe file. Finally, we can look at all environment variables:

```
client.environment
{'SCIF_APPBIN_hello_world_echo': '/scif/apps/hello-world-echo/bin',
 'SCIF_APPBIN_hello_world_script': '/scif/apps/hello-world-script/bin',
 'SCIF_APPDATA_hello_world_echo': '/scif/data/hello-world-echo',
 'SCIF_APPDATA_hello_world_script': '/scif/data/hello-world-script',
 'SCIF_APPENV_hello_world_echo': '/scif/apps/hello-world-echo/scif/environment.sh',
 'SCIF_APPENV_hello_world_script': '/scif/apps/hello-world-script/scif/environment.sh',
 'SCIF_APPHELP_hello_world_echo': '/scif/apps/hello-world-echo/scif/runscript.help',
 'SCIF_APPHELP_hello_world_script': '/scif/apps/hello-world-script/scif/runscript.help',
 'SCIF_APPLABELS_hello_world_echo': '/scif/apps/hello-world-echo/scif/labels.json',
 'SCIF_APPLABELS_hello_world_script': '/scif/apps/hello-world-script/scif/labels.json',
 'SCIF_APPLIB_hello_world_echo': '/scif/apps/hello-world-echo/lib',
 'SCIF_APPLIB_hello_world_script': '/scif/apps/hello-world-script/lib',
 'SCIF_APPMETA_hello_world_echo': '/scif/apps/hello-world-echo/scif',
 'SCIF_APPMETA_hello_world_script': '/scif/apps/hello-world-script/scif',
 'SCIF_APPNAME_hello_world_echo': 'hello-world-echo',
 'SCIF_APPNAME_hello_world_script': 'hello-world-script',
 'SCIF_APPRECIPE_hello_world_echo': '/scif/apps/hello-world-echo/scif/hello-world-echo.scif',
 'SCIF_APPRECIPE_hello_world_script': '/scif/apps/hello-world-script/scif/hello-world-script.scif',
 'SCIF_APPROOT_hello_world_echo': '/scif/apps/hello-world-echo',
 'SCIF_APPROOT_hello_world_script': '/scif/apps/hello-world-script',
 'SCIF_APPRUN_hello_world_echo': '/scif/apps/hello-world-echo/scif/runscript',
 'SCIF_APPRUN_hello_world_script': '/scif/apps/hello-world-script/scif/runscript',
 'SCIF_APPS': '/scif/apps',
 'SCIF_DATA': '/scif/data'}
```

You will notice of an absence of variables that aren't relative to one of our apps (e.g., we don't see `SCIF_APPNAME` without `hello_world_echo` or `hello_world_script`), and this is because we are running the shell that doesn't have the context of a particular SCIF app. If you wanted to activate an app, which comes down to exporting its environment, just ask for it:

```
client.activate('hello-world-script')
```

You can also do this directly from the terminal by giving pyshell the app name:

```
$ scif pyshell hello-world.scif hello-world-echo
[scif] /scif hello-world-echo | hello-world-script
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client._active
Out[1]: 'hello-world-echo'
```

In both cases, when we look at the environment we see what we saw before, but we also see another set of environment variables with general names (e.g. `SCIF_APPBIN`) that are pointing to the active app, which in this case, is `hello-world-echo`

```
$ client.environment

{'SCIF_APPBIN': '/scif/apps/hello-world-echo/bin',
 'SCIF_APPDATA': '/scif/data/hello-world-echo',
 'SCIF_APPENV': '/scif/apps/hello-world-echo/scif/environment.sh',
 'SCIF_APPHELP': '/scif/apps/hello-world-echo/scif/runscript.help',
 'SCIF_APPLABELS': '/scif/apps/hello-world-echo/scif/labels.json',
 'SCIF_APPLIB': '/scif/apps/hello-world-echo/lib',
 'SCIF_APPMETA': '/scif/apps/hello-world-echo/scif',
 'SCIF_APPNAME': 'hello-world-echo',
 'SCIF_APPRECIPE': '/scif/apps/hello-world-echo/scif/hello-world-echo.scif',
 'SCIF_APPROOT': '/scif/apps/hello-world-echo',
 'SCIF_APPRUN': '/scif/apps/hello-world-echo/scif/runscript',
 'SCIF_APPS': '/scif/apps',
 'SCIF_DATA': '/scif/data'
  ...
}
```

The reason that we have both is, you can imagine a case where you want to run one SCIF app, and while it's running, have it interact in some way with another known app. Given the information about other apps is exposed in the environment, this is possible to do! You can reference an app environment variable in another's runscript. Here are some fun examples:

```
# have running foo call bar's runscript
%apprun foo
/bin/bash $SCIF_APPRUN_bar

# source bar's environment first, then run it
%apprun foo
source $SCIF_APPENV_bar
/bin/bash $SCIF_APPRUN_bar
```

Having these general environment variables for the active app also ensures that a tool created to work with SCIF applications knows how to find the active application. For example, let's say I create an app that anyone can install into a container, and it only serves to loop through all the other apps and parse the text content of the runscript for some kind of machine learning algorithm? I'd be able to discovery them all without much work, and without knowing anything about the particular apps installed:

```
# This gives me the runscript locations
env | grep SCIF_APPRUN
SCIF_APPRUN_hello_world_script=/scif/apps/hello-world-script/scif/runscript
SCIF_APPRUN_hello_world_echo=/scif/apps/hello-world-echo/scif/runscript
```

I could also blindly parse through help files, environments, labels, or any other content that is programatically accessible! You don't need to know anything in advance beyond these SCIF variables to interact with scientific filesystems. We will go into more command examples as we progress in these tutorials, let's continue now and talk about how to build a SCIF into a container, which is the recommended approach for reproducibility.


## Install SCIF in Docker using Recipe
Once we have previewed, we likely want to install. I'm not a fan of making changes on my host, so I'm going to test doing this inside of a Docker image. First we will do it interactively, and then add a few lines to a recipe to do it properly. Here is the interactive version. We will use an anaconda image so we know that it comes with pip to install `scif`. Note that I'm mapping the present working directory to `/tmp` so I have my `hello-world.scif` recipe.

```
$ docker run -v $PWD:/tmp -it continuumio/anaconda3 /bin/bash
$ pip install scif
$ scif install hello-world.scif 
Installing base at /scif
+ apprun hello-world-echo
+ appenv hello-world-echo
+ apprun hello-world-script
+ appenv hello-world-script
+ appinstall hello-world-script
```

the same can be done from within the shell:

```
client.install()
Installing base at /scif
+ apprun hello-world-echo
+ appenv hello-world-echo
+ apprun hello-world-script
+ appenv hello-world-script
+ appinstall hello-world-script
```

and then we can see the tree hierarchies for the top level folders and apps

```
# apt-get install -y tree

$ tree /scif/
/scif/
├── apps
│   ├── hello-world-echo
│   │   ├── bin
│   │   ├── lib
│   │   └── scif
│   │       ├── environment.sh
│   │       ├── hello-world-echo.scif
│   │       └── runscript
│   └── hello-world-script
│       ├── bin
│       ├── lib
│       └── scif
│           ├── environment.sh
│           ├── hello-world-script.scif
│           └── runscript
└── data
    ├── hello-world-echo
    └── hello-world-script
```

Want to see the apps installed more quickly than using tree?

```
scif apps
SCIF [app]              [root]
1  hello-world-script	/scif/apps/hello-world-script
2  hello-world-echo	/scif/apps/hello-world-echo
```

If we had done this before install, we would get a *ruhroh* message.

```
$ scif apps
WARNING /scif is not detected as a recipe or base.
```

We have a scientific filesystem ready to go! At this point, if you want this generation to be reproducible, you need to generate a build specification (a [Dockerfile](Dockerfile)) to build the container above.


```
FROM continuumio/anaconda3
RUN pip install scif
ADD hello-world.scif
RUN scif install /hello-world.scif
CMD ["scif"]
```

and then we could build that:

```
docker build -t vanessa/scif .
```

and run it to see the help:

```
docker run -it vanessa/scif
```

We will review more interesting commands and interaction with your SCIF in the next tutorial on how to [run SCIF](tutorial-run.md). This tutorial will finish to show installation in a Singularity container, followed by reverse engineer of a recipe from a SCIF.


## Install SCIF in Singularity Natively 
Singularity containers, in that they are optimized for scientific reproducibility, work extremely well with SCIF. When you build a Singularity container you create a squashfs filesystem that isn't writable after build time, and so you can have confidence that the contents of your container will not be modified. The second important note is that Singularity has native integration for SCIF, meaning you can write the recipe directly into the build file! Let's take a look at our hello world example above, but writing into a [Singularity](Singularity) build file:


```
Bootstrap: docker
From: continuumio/anaconda3

# sudo singularity build hello-world.simg Singularity

########################################################
##
## SCIF:
##
## These sections are equivalent to a SCIF Recipe
##
########################################################

%appenv hello-world-echo
    THEBESTAPP=$SCIF_APPNAME
    export THEBESTAPP
%apprun hello-world-echo
    echo "The best app is $THEBESTAPP"

%appinstall hello-world-script
    echo "echo 'Hello World!'" >> bin/hello-world.sh
    chmod u+x bin/hello-world.sh
%appenv hello-world-script
    THEBESTAPP=$SCIF_APPNAME
    export THEBESTAPP
%apprun hello-world-script
    /bin/bash hello-world.sh
```

Notice the following:
 
  1. we have literally copied the recipe into the Singularity build file (middle section) and we are using the same image base (`continuumio/anaconda3`) as we did for Docker. I also like to use the `continuumio/miniconda3` container for a tinier conda snake :).
  2. We are not installing the scif software anywhere. Singularity has the integration natively.

```
sudo singularity build hello-world.simg Singularity
```

And then we would run a particular app as follows:

```
# hello-world-script
singularity run --app hello-world-script hello-world.simg 
Hello World!

# hello-world-echo
$ singularity run --app hello-world-echo hello-world.simg 
The best app is hello-world-echo

# no app specified (runscript)
$ singularity run hello-world.simg 
$
```

For the last example, you don't see any obvious change in output because we've merely shelled into the container! If you had defined a Singularity `%runscript` section with a different command, it would be issued instead. If you are using the `scif` software as a driver, you could export `SCIF_ENTRYPOINT` to define a different command from the default of `/bin/bash`.


## Install SCIF in Singularity using Recipe
You can install use SCIF within Singularity containers using the scif software (akin to what we did with Docker. For this example, the [Singularity build specification](Singularity.scif) would be adjusted to look like this:


```
Bootstrap: docker
From: continuumio/anaconda3

# sudo singularity build hello-world-scif.simg Singularity.scif

%files
    hello-world.scif

%environment
    PATH=/opt/conda/bin:$PATH
    export PATH

%post
    /opt/conda/bin/pip install scif
    /opt/conda/bin/scif install /hello-world.scif

%runscript
    exec scif "$@"
```

Notice how we are again just copying the recipe file into the container, installing scif, and then handing the container's entrypoint to scif to manage. I'm being very careful to add executables to the path and reference them directly, in the case that some future user might have a different version of the software installed locally. Any similar container or virtalization technology that follows these steps could support SCIF. To build the container, again we do:

```
sudo singularity build hello-world-scif.simg Singularity.scif
```


## Reverse engineer Recipe from SCIF
Finally, given that you have an existing scientific filesystem, you can easily produce its recipe file from the various metadata folders that are discovered, and given that the creator has not changed this content manually, although you can't have guarantee that it's reproducible, there is a good chance given all previous depdendencies are still available. Let's use the container that we generated above, specifically with the command `inspect` to take a look, and then `dump` to export the recipe. First, you can inspect an entire filesystem and get the results in json printed to the screen:

```
scif inspect 
{
    "hello-world-script": {
        "appinstall": [
            "echo \"echo 'Hello World!'\" >> $SCIF_APPBIN/hello-world.sh",
            "chmod u+x $SCIF_APPBIN/hello-world.sh"
        ],
        "appenv": [
            "THEBESTAPP $SCIF_APPNAME"
        ],
        "apprun": [
            "/bin/bash hello-world.sh"
        ]
    },
    "hello-world-echo": {
        "appenv": [
            "THEBESTAPP $SCIF_APPNAME"
        ],
        "apprun": [
            "echo \"The best app is $THEBESTAPP\""
        ]
    }
}
```

And then dump the same content as a recipe:


```
scif dump
%appinstall
echo "echo 'Hello World!'" >> $SCIF_APPBIN/hello-world.sh
chmod u+x $SCIF_APPBIN/hello-world.sh

%appenv
THEBESTAPP $SCIF_APPNAME

%apprun
/bin/bash hello-world.sh

%appenv
THEBESTAPP $SCIF_APPNAME

%apprun
echo "The best app is $THEBESTAPP"
```

Now that you've gotten a hang for writing recipes, previewing and installing SCIF, let's move on to look at some [commands](/scif/tutorial-commands).
