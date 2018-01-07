---
layout: default
title: Interaction with the Scientific Filesystem
pdf: true
permalink: /tutorial-commands
toc: false
---

At this point, you are comfortable with [preview or install](/scif/tutorial-preview-install) of a SCIF, and are ready for more advanced interaction. This means any of the following commands, and some of these have already been demonstrated in the previous tutorial, and will have detail added here:

 - **apps**
 - **inspect**
 - **shell**
 - **run**
 - **exec**

## Apps
Apps will give you a simple listing of apps installed.

```
$ scif apps
SCIF [app]              [root]
1  hello-world-script	/scif/apps/hello-world-script
2  hello-world-echo	/scif/apps/hello-world-echo
```

and if you don't have any installed, you get a warning instead.

```
WARNING /scif is not detected as a recipe or base.
```

## Inspect
Inspect is what you want to use to look at different metadata about a SCIF or app within it. Without any arguments, you will get json output for all apps installed in your SCIF:

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

If you add the name of an app, you will filter the output to it:

```
scif inspect hello-world-echo
{
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

If you add a particular attribute, you can further filter the result. For attributes your choices are `a` (all) `l` (labels) `e` (environment) `r` (runscript) `f` (files) or `i` (install). Here we ask to see the runscript (`r`)

```
scif inspect hello-world-echo r
{
    "hello-world-echo": {
        "apprun": [
            "echo \"The best app is $THEBESTAPP\""
        ]
    }
}
```

Finally, to dump the original recipe, just use "dump":

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

## Pyshell
Pyshell produces an interactive python terminal to work with your SCIF. As we saw previously, depending on whether you provide a recipe, an app, or both, you get different environments to work in. This is entry to a python interactive shell.


### SCIF python shell Options

|  example            | use case                                | 
|---------------------|-------------------------------------------|
| scif pyshell [recipe] | interact with a recipe, no changes to the filesystem (akin to preview) |
| scif pyshell          | interact with a SCIF (no SCIF app active) |
| scif pyshell [app]    | interact with a SCIF with an app active.  |
| scif pyshell [recipe] [app]    | interact with a recipe, still no changes, but load context of an app|

If you want to change the default shell used, set the variable `SCIF_SHELL`. For default it will use `/bin/bash`.


## Shell
Running a standard shell means bash in the context of an app, meaning a subprocess for `/bin/bash` (default determined by the environment variable `SCIF_PYSHELL` during runtime). We aren't in any sort of container, so there is no context of shell in the way you would think of shelling into a container or running SSH to connect to a server. This is entry to a bash shell.

### SCIF shell Options

|  example            | use case                                | 
|---------------------|-------------------------------------------|
| scif shell          | interact with a SCIF (no SCIF app active) |
| scif shell [app]    | interact with a SCIF with an app active.  |

From the above, we can see that it's possible to shell into only a context, meaning the context of an installed app, or the entire filesystem. Physically shelling into a recipe (a file system that doesn't exist yet) doesn't make sense.


## Run
The run command will explicity run the script provided in the `apprun` section.  In our example, running `hello-world-echo` will echo "Hello World" to the console.

```
$ scif run hello-world-echo
[hello-world-echo] executing /bin/bash /scif/apps/hello-world-echo/scif/runscript
The best app is hello-world-echo
```

Running the second app, `hello-world-script`, is actually a very cool example because in it we are calling a script that was written via an echo during the install step. If you remember:

```
%appinstall hello-world-script
    echo "echo 'Hello World!'" >> $SCIF_APPBIN/hello-world.sh
    chmod u+x $SCIF_APPBIN/hello-world.sh
```
and then running it:

```
%apprun hello-world-script
    /bin/bash hello-world.sh
```
This means the following:

 - we have the variable `SCIF_APPBIN` on the path for our usage during install.
 - we also have the `SCIF_APPBIN` added to the `PATH` for runtime, so the script is found period. 

Awesome!

If an app doesn't have an `%apprun` section, we default to a shell. For example, here is a third app that I added to install that is just an environment

```
%appenv hello-world-env
    OMG=TACOS

# then scif install hello-world.scif again

scif install hello-world.scif hello-world-env
Installing base at /scif
+ appenv hello-world-env
```

if we run the app, we get a shell.

```
$ scif run hello-world-env
[hello-world-env] executing /bin/bash 
$/scif/apps/hello-world-env# echo $OMG
TACOS
```

Again, cool! This example also nicely shows how an entire app can just be an environment context. Now it's time to look at executing commands with "exec."


## Exec
Let's take the `hello-world-echo` app as an example. When we shell with context of this app, we would expect its environment variables to be active. Can we show that with exec?

```
$ scif exec hello-world-echo echo The best app is $THEBESTAPP
[hello-world-echo] executing /bin/echo
The best app is 
```

Ruhroh! No output! The reason is because the variable gets evaluated *before* getting parsed in. To get around this, we have a special syntax to distinguish an environment variable. Try this!

```
$ scif exec hello-world-echo echo The best app is [e]THEBESTAPP
[hello-world-echo] executing /bin/echo The best app is $THEBESTAPP
The best app is hello-world-echo
```

This little bug has always been a pet peeve of mine, so I've introduced the little `[e]` so we don't have to struggle.

More coming soon!
