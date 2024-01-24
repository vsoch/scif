# Exit Code from run

This should be built from the root of the repository as follows:

```
# apptainer build scif.sif docs/examples/exit-from-run/apptainer.def 
```

The force_fail app returns exit code 155
```
$ apptainer run scif.sif run force_fail ; echo "Exit Code: $?";
[force_fail] executing /bin/bash /scif/apps/force_fail/scif/runscript
Calling exit 155
ERROR Return code 155
Exit Code: 155
```

The 'success' app returns exit code 0

```
$ apptainer run scif.sif run success ; echo "Exit Code: $?";
[success] executing /bin/bash /scif/apps/success/scif/runscript
Running successfully
Exit Code: 0
```
