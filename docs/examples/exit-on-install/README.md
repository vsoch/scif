# Exit on Install

This should be built from the root of the repository as follows:

```bash
docker build -f docs/examples/exit-on-install/Dockerfile -t scif-exit-on-install .
```

When you build the above, it should exit on the install of one of the apps:

```bash
Using /opt/conda/lib/python3.7/site-packages
Finished processing dependencies for scif==0.0.81
Removing intermediate container adef9b9e2880
 ---> 1827c8e9dfde
Step 5/7 : ENV PATH=/opt/conda/bin:$PATH
 ---> Running in 02f699d02f52
Removing intermediate container 02f699d02f52
 ---> 6916a222e1c6
Step 6/7 : RUN scif install /code/docs/examples/exit-on-install/recipe.scif
 ---> Running in 30639ab520f0
ERROR Return value 256 for install of hello-world-script
Installing base at /scif
+ apprun     hello-world-echo
+ appenv     hello-world-echo
+ apprun     hello-world-script
+ appenv     hello-world-script
+ apphelp     hello-world-script
+ appinstall hello-world-script
The command '/bin/sh -c scif install /code/docs/examples/exit-on-install/recipe.scif' returned a non-zero code: 1
```
The user is alerted of the error here:

```bash
ERROR Return value 256 for install of hello-world-script
```
