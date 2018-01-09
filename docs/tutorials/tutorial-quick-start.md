---
layout: default
title: The Scientific Filesystem Quick Start
pdf: true
permalink: /tutorial-quick-start
toc: false
---

# Scientific Filesystem Quick Start
This is the quick start for using a Scientific Filesystem. We won't be designing or creating one, but using a pre-generated Docker or Singularity container. The awesome part is that despite two different container technologies, the guts inside, and interacting with them, will be the same! Thus, we will first show how to pull the different containers, and then show usage side by side. If you *do* want to learn these first steps, see the [preview and install tutorial](/scif/tutorial-preview-install).

What you should understand for this quick start is what we've done thus far. We (as the *creator* of a container with a scientific filesystem) wrote a recipe, a text file with instructions for interacting with different scientific filesystem software modules ("apps") and then exposed a single entrypoint that is the controller for the different apps. Then we build the container.

Then the *user* that doesn't have knowledge to the creation is able to interact with the software modules defined by the filesystem in a consistent and user friendly way. Right now I am playing the role of the creator, and you the user for doing this quick start. Let's jump in!


## Singularity
For our first container we are using the Singularity scientific filesystem container that is built in the [preview and install](/scif/tutorial-preview-install#install-scif-in-singularity-using-recipe) tutorial. First, you should pull the image, either with the [sregistry client](https://singularityhub.github.io/sregistry-cli) or singularity natively:

```
singularity pull --name scif-cli shub://vsoch/scif:scif
Progress |===================================| 100.0% 
Done. Container is at: /home/vanessa/Desktop/scif-cli

# or using sregistry client
# sregistry pull --name scif-cli vsoch/scif:scif
```

**Importantly** note that we are pulling the tag `scif`. If you pull latest (e.g., `vsoch/scif` then you will get a container with the scif client installed, but no fliesystem.


## Docker
For our second container, we are starting with the Dockerized scientific filesystem container that is built in the [preview and install](/scif/tutorial-preview-install#install-scif-in-docker-using-recipe) tutorial. We will use the latest for this example, and you can also see the [tags available](https://hub.docker.com/r/vanessa/scif/tags/) for other versions. First, pull the image:

```
docker pull vanessa/scif
```

What you should understand from the install tutorial is that we (as the *creator* of the container) wrote a recipe, a text file with instructions for interacting with different scientific filesystem software modules ("apps") and then exposed a single entrypoint that is the controller for the different apps. Then we build the container.

Then the *user* that doesn't have knowledge to the creation is able to interact with the software modules defined by the filesystem in a consistent and user friendly way. Right now I am playing the role of the creator, and you the user. Let's jump in! For each example below, you can test with Docker, Singularity, or both. For some, the `$PS1` prompt might not match, but the output is equivalent.


### Test the entrypoint
We can first test the entrypoint. We have just pulled the container, and we know nothing. So we run it.

```
docker run vanessa/scif
```

```
./scif-cli 

Scientific Filesystem [v0.0.3]
usage: scif [-h] [--debug] [--quiet] [--writable]
            {version,pyshell,shell,preview,help,install,inspect,run,apps,dump,exec}
            ...

scientific filesystem tools

optional arguments:
  -h, --help            show this help message and exit
  --debug               use verbose logging to debug.
  --quiet               suppress print output
  --writable, -w        for relevant commands, if writable SCIF is needed

actions:
  actions for Scientific Filesystem

  {version,pyshell,shell,preview,help,install,inspect,run,apps,dump,exec}
                        scif actions
    version             show software version
    pyshell             Interactive python shell to scientific filesystem
    shell               shell to interact with scientific filesystem
    preview             preview changes to a filesytem
    help                look at help for an app, if it exists.
    install             install a recipe on the filesystem
    inspect             inspect an attribute for a scif installation
    run                 entrypoint to run a scientific filesystem
    apps                list apps installed
    dump                dump recipe
    exec                execute a command to a scientific filesystem
```

### Apps
We are familiar with the scientific filesystem, so we can use the `apps` command to see what is installed. Since this conainer had the scientific filesystem installed on build, it already has three apps for us to play with:


```
docker run vanessa/scif apps
```

```
./scif-cli apps

SCIF [app]              [root]
1  hello-world-env	/scif/apps/hello-world-env
2  hello-world-script	/scif/apps/hello-world-script
3  hello-world-echo	/scif/apps/hello-world-echo
```

### Help
We can then ask for help for a particular app. This section is important for the creator to put some time into describing the basic important things that should be known.

```
docker run vanessa/scif help hello-world-env
```

```
./scif-cli help hello-world-env
This is the help section for hello-world-env! This app
does not have anything other than an environment installed.
It just defines the environment variable `OMG=TACOS`. Try issuing
a command to the scif entrypoint to echo this variable:
scif exec hello-world-env echo [e]OMG
docker run vanessa/scif exec hello-world-env echo [e]OMG
[hello-world-env] executing /bin/echo $OMG
TACOS
```

And you see a hasty help message that I wrote for the module `hello-world-env` telling you how to run it. We will do that soon.


### Inspect
We can also inspect an app of interest, which will spit out a metadata structure for it. You can think of the help command as returning a human friendly thing, and inspect something that can be programmatically parsed.


```
docker run vanessa/scif inspect hello-world-env
```

```
./scif-cli inspect hello-world-env
{
    "hello-world-env": {
        "appenv": [
            "OMG=TACOS"
        ],
        "apphelp": [
            "This is the help section for hello-world-env! This app",
            "does not have anything other than an environment installed.",
            "It just defines the environment variable `OMG=TACOS`. Try issuing",
            "a command to the scif entrypoint to echo this variable:",
            "scif exec hello-world-env echo [e]OMG",
            "docker run vanessa/scif exec hello-world-env echo [e]OMG",
            "[hello-world-env] executing /bin/echo $OMG",
            "TACOS"
        ]
    }
}
```

Yes, it really just is an environment, and a help message for it! Now that we've seen this instruction twice, let's give run a try with specification of an environment variable, `$OMG` in the container.

### Run
We can run the `hello-world-echo` app like this:

```
docker run vanessa/scif run hello-world-echo
```

```
./scif-cli run hello-world-echo
[hello-world-echo] executing /bin/bash /scif/apps/hello-world-echo/scif/runscript
The best app is hello-world-echo
```

What about our example above with `hello-world-env`? It can be weird trying to pass an environment variable into a container from the host, because it gets evaluated (and then winds up something unexpected or empty!) To help this, with scif we use a modified syntax to pass the variable into the container. We replace `$` with `[e]` so that `$VARIABLE` is `[e]VARIABLE`. Here is an example:

```
docker run vanessa/scif exec hello-world-env echo [e]OMG
```
```
./scif-cli exec hello-world-env echo [e]OMG
[hello-world-env] executing /bin/echo $OMG
TACOS
```

If we had done that with `$` it would have evaluated the variable on our host shell, and passed nothing into the container (unless in fact `$OMG` was defined on the host)/

### Exec
You can also execute a command:

```
docker run vanessa/scif exec hello-world-echo echo "Another hello!"
```

```
./scif-cli exec hello-world-echo echo "Another hello!"
[hello-world-echo] executing /bin/echo Another hello!
Another hello!
```


## Bash Shell
If you want to interact with your container in the context of an app, there is a command for that!  We can either shell into the container with the global scif environment (and no activated apps):

```
./scif-cli shell
```

```
docker run -it vanessa/scif shell
WARNING No app selected, will run default ['/bin/bash']
executing /bin/bash 
root@1ab15ba4cc3b:/scif
$ ls
apps
data
```

or we can do the same in the context of a specific app:


```
./scif-cli shell hello-world-env
```

```
docker run -it vanessa/scif shell hello-world-env
[hello-world-env] executing /bin/bash 
root@1ab15ba4cc3b:/scif/apps/hello-world-env# echo $OMG
TACOS
root@1ab15ba4cc3b:/scif/apps/hello-world-env# 
```

This is a great example of how a single container can be used to serve different interactive environments.


## Python Shell
We can enter an interactive shell for exploring the container filesystem, if we want to do more than execute commands. For docker, we have to append an `-it` to mean we want an "interactive terminal" to the run command, using "pyshell" as the entrypoint:

```
./scif-cli pyshell
Found configurations for 2 scif apps
hello-world-echo
hello-world-script
[scif] /scif hello-world-echo | hello-world-script
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.
```

```
docker run -it vanessa/scif pyshell
Found configurations for 3 scif apps
hello-world-env
hello-world-script
hello-world-echo
[scif] /scif hello-world-env | hello-world-script | hello-world-echo
Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.
```

We can now look at details for the client:

```
In [1]: client
Out[1]: [scif]

In [2]: client.apps()
Out[2]: ['hello-world-env', 'hello-world-script', 'hello-world-echo']
```

The "preview" command is most useful when you have a recipe (and haven't installed yet) and want to look at what will be created on the filesystem. But you can also run it for an already installed scif:

```
In [3]: client.preview()
[base] /scif 
[apps] /scif/apps 
[data] /scif/data
 

[root] /scif/apps/hello-world-env 
[lib] /scif/apps/hello-world-env/lib 
[bin] /scif/apps/hello-world-env/bin 
[data] /scif/data/hello-world-env 
+ appenv hello-world-env
/scif/apps/hello-world-env/scif/environment.sh
OMG=TACOS
+ apprecipe hello-world-env
/scif/apps/hello-world-env/scif/hello-world-env.scif

...
```

You can also get the full set of environment variables:

```
client.get_env()
Out[5]: 
{'SCIF_APPBIN_hello_world_echo': '/scif/apps/hello-world-echo/bin',
 'SCIF_APPBIN_hello_world_env': '/scif/apps/hello-world-env/bin',
 'SCIF_APPBIN_hello_world_script': '/scif/apps/hello-world-script/bin',
 'SCIF_APPDATA_hello_world_echo': '/scif/data/hello-world-echo',
 'SCIF_APPDATA_hello_world_env': '/scif/data/hello-world-env',
 'SCIF_APPDATA_hello_world_script': '/scif/data/hello-world-script',
 'SCIF_APPENV_hello_world_echo': '/scif/apps/hello-world-echo/scif/environment.sh',
 'SCIF_APPENV_hello_world_env': '/scif/apps/hello-world-env/scif/environment.sh',
 'SCIF_APPENV_hello_world_script': '/scif/apps/hello-world-script/scif/environment.sh',
 'SCIF_APPHELP_hello_world_echo': '/scif/apps/hello-world-echo/scif/runscript.help',
 'SCIF_APPHELP_hello_world_env': '/scif/apps/hello-world-env/scif/runscript.help',
 'SCIF_APPHELP_hello_world_script': '/scif/apps/hello-world-script/scif/runscript.help',
 'SCIF_APPLABELS_hello_world_echo': '/scif/apps/hello-world-echo/scif/labels.json',
 'SCIF_APPLABELS_hello_world_env': '/scif/apps/hello-world-env/scif/labels.json',
 'SCIF_APPLABELS_hello_world_script': '/scif/apps/hello-world-script/scif/labels.json',
 'SCIF_APPLIB_hello_world_echo': '/scif/apps/hello-world-echo/lib',
 'SCIF_APPLIB_hello_world_env': '/scif/apps/hello-world-env/lib',
 'SCIF_APPLIB_hello_world_script': '/scif/apps/hello-world-script/lib',
 'SCIF_APPMETA_hello_world_echo': '/scif/apps/hello-world-echo/scif',
 'SCIF_APPMETA_hello_world_env': '/scif/apps/hello-world-env/scif',
 'SCIF_APPMETA_hello_world_script': '/scif/apps/hello-world-script/scif',
 'SCIF_APPNAME_hello_world_echo': 'hello-world-echo',
 'SCIF_APPNAME_hello_world_env': 'hello-world-env',
 'SCIF_APPNAME_hello_world_script': 'hello-world-script',
 'SCIF_APPRECIPE_hello_world_echo': '/scif/apps/hello-world-echo/scif/hello-world-echo.scif',
 'SCIF_APPRECIPE_hello_world_env': '/scif/apps/hello-world-env/scif/hello-world-env.scif',
 'SCIF_APPRECIPE_hello_world_script': '/scif/apps/hello-world-script/scif/hello-world-script.scif',
 'SCIF_APPROOT_hello_world_echo': '/scif/apps/hello-world-echo',
 'SCIF_APPROOT_hello_world_env': '/scif/apps/hello-world-env',
 'SCIF_APPROOT_hello_world_script': '/scif/apps/hello-world-script',
 'SCIF_APPRUN_hello_world_echo': '/scif/apps/hello-world-echo/scif/runscript',
 'SCIF_APPRUN_hello_world_env': '/scif/apps/hello-world-env/scif/runscript',
 'SCIF_APPRUN_hello_world_script': '/scif/apps/hello-world-script/scif/runscript',
 'SCIF_APPS': '/scif/apps',
 'SCIF_DATA': '/scif/data'}
```

or activate an app (and then see how the enviroment variables change, they will have added a few!

```
client.activate('hello-world-env')

In [7]: client.get_env()
Out[7]: 
{'OMG': 'TACOS',
 'SCIF_APPBIN': '/scif/apps/hello-world-env/bin',
 'SCIF_APPDATA': '/scif/data/hello-world-env',
 'SCIF_APPENV': '/scif/apps/hello-world-env/scif/environment.sh',
 'SCIF_APPHELP': '/scif/apps/hello-world-env/scif/runscript.help',
 'SCIF_APPLABELS': '/scif/apps/hello-world-env/scif/labels.json',
 'SCIF_APPLIB': '/scif/apps/hello-world-env/lib',
 'SCIF_APPMETA': '/scif/apps/hello-world-env/scif',
 'SCIF_APPNAME': 'hello-world-env',
  ...
 'SCIF_APPRECIPE': '/scif/apps/hello-world-env/scif/hello-world-env.scif',
 'SCIF_APPROOT': '/scif/apps/hello-world-env',
 'SCIF_APPRUN': '/scif/apps/hello-world-env/scif/runscript',
 'SCIF_APPS': '/scif/apps',
 'SCIF_DATA': '/scif/data'}
```

And then deactivate to undo that.

```
client.deactivate()
```

I'm skiing over sunshine with happiness to be working on this! The response to reviewers (with this update) will be submit in early March. Please contribute feedback (no matter how small!) to the [docs, spec, or the client](https://github.com/vsoch/scif) (all served from that repo) and add your name to the [specification](https://github.com/vsoch/scif/blob/master/docs/spec/spec.md). If you have *already contributed*, then please submit a pull request there and add your name! I will be designing a nice logo and adding more examples and updates in a few weeks after a brief hiatus. Onwards to scientific filesystem galaxies, friends!
