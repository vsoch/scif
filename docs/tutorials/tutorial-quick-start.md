---
layout: default
title: The Scientific Filesystem Quick Start
pdf: true
permalink: /tutorial-quick-start
toc: false
---

## What you start with
We are starting with the Dockerized scientific filesystem container that is built in the [preview and install](/scif/tutorial-preview-install#install-scif-in-docker-using-recipe) tutorial. We will use the latest for this example, and you can also see the [tags available](https://hub.docker.com/r/vanessa/scif/tags/) for other versions. First, pull the image:

```
docker pull vanessa/scif
```

What you should understand from the install tutorial is that we (as the *creator* of the container) wrote a recipe, a text file with instructions for interacting with different scientific filesystem software modules ("apps") and then exposed a single entrypoint that is the controller for the different apps. Then we build the container.

Then the *user* that doesn't have knowledge to the creation is able to interact with the software modules defined by the filesystem in a consistent and user friendly way. Right now I am playing the role of the creator, and you the user. Let's jump in!

### Test the entrypoint
We can first test the entrypoint. We have just pulled the container, and we know nothing. So we run it.

```
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
We are familiar with the scientific filesystem, so we can use the `apps` command to see what is installed.

```
docker run vanessa/scif apps
SCIF [app]              [root]
1  hello-world-env	/scif/apps/hello-world-env
2  hello-world-script	/scif/apps/hello-world-script
3  hello-world-echo	/scif/apps/hello-world-echo
```

### Help
We can then ask for help for a particular app. This section is important for the creator to put some time into describing the basic important things that should be known.

```
docker run vanessa/scif help hello-world-env

   This is the help section for hello-world-env! This app
   does not have anything other than an environment installed. 
   It just defines the environment variable `OMG=TACOS`. Try issuing
   a command to the scif entrypoint to echo this variable:

        # Local installation
        scif exec hello-world-env echo [e]OMG
        
        # Docker image example
        docker run vanessa/scif exec hello-world-env echo [e]OMG
        [hello-world-env] executing /bin/echo $OMG
        TACOS
```


### Inspect
We can also inspect an app of interest, which will spit out a metadata structure for it. You can think of the help command as returning a human friendly thing, and inspect something that can be programmatically parsed.


```
 docker run vanessa/scif inspect hello-world-env
{
    "hello-world-env": {
        "appenv": [
            "OMG=TACOS"
        ]
    }
}
```

Yes, it really just is an environment!


### Run
Now that you have listed and inspected an app, let's run one! We can run the `hello-world-echo` app like this:

```
docker run vanessa/scif run hello-world-echo
[hello-world-echo] executing /bin/bash /scif/apps/hello-world-echo/scif/runscript
The best app is hello-world-echo
```

### Exec
You can also execute a command:

```
docker run vanessa/scif exec hello-world-echo echo "Another hello!"
[hello-world-echo] executing /bin/echo Another hello!
Another hello!
```

### Environment variables
It can be weird trying to pass an environment variable into a container from the host, because it gets evaluated (and then winds up something unexpected or empty!) To help this, with scif we use a modified syntax to pass the variable into the container. We replace `$` with `[e]` so that `$VARIABLE` is `[e]VARIABLE`. Here is an example:

```
docker run vanessa/scif exec hello-world-env echo [e]OMG
[hello-world-env] executing /bin/echo $OMG
TACOS
```
If we had done that with `$` it would have evaluated the variable on our host shell, and passed nothing into the container (unless in fact `$OMG` was defined on the host)/
