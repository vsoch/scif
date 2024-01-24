# Exit Code from run

This should be built from the root of the repository as follows:

```bash
apptainer build docs/examples/exit-from-run/apptainer.def scif.sif
apptainer run scif.sif run force_failure || echo "Got non-zero exit code: $?  Success!"

```


