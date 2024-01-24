# Exit Code from run

This should be built from the root of the repository as follows:

```
# apptainer build scif.sif docs/examples/exit-from-run/apptainer.def 
```

The force_fail app returns exit code 155
```
# apptainer run scif.sif run force_fail ; echo "Out: $?"
[force_fail] executing /bin/bash /scif/apps/force_fail/scif/runscript
ERROR Return code 155
Out: 155
```

The 'success' app returns exit code 0

```
$ apptainer run scif.sif run success ; echo "Out: $?"
[success] executing /bin/bash /scif/apps/success/scif/runscript
Out: 0
```
