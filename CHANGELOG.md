# CHANGELOG

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented by the pull requests that fixed them.

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes
 - changed behaviour

Versions in parentheses coincide with what is available on [pypi](https://pypi.org/project/scif/).

## [xxx](https://github.com/vsoch/scif/tree/master) (master)
 - install return value non zero should stop build (0.0.81)
 - removing Python less than 3.6 support (0.0.80)
 - code formatting with black, shell entrypoint bug (0.0.79)
 - executable not found, will not run, adding streaming to output (0.0.78)
 - args not passed correctly for run and exec (0.0.77)
 - test and runscript need to be executable after write (0.0.76)
 - fixing bug that None can go into function to test app (0.0.75)
 - adding test to client, along with tests for functions (and on CircleCI) (0.0.74)
 - ensuring that other application environment variables available at install (0.0.73)
 - adding custom shell command to client, and ensuring paths get appended (0.0.72)
 - allowing support for periods in app names (0.0.71)
 - fixing bug with adding files to appbase, shouldn't change directory (0.0.70)
 - updates to source environment correctly (0.0.69)
 - added append sticker (`[append]` for `>>`) (0.0.68)
 - adding scif stamps for pipes [pipe], and in/output direction [out]/[in] (0.0.67)
 - fixing bug that arguments (--) don't get passed through to exec/run (0.0.65)
 - copying of files should be relative to app folder (0.0.58)
 - fixed bug that install with python2 cannot use "exec" (0.0.55)
 - fixed bug in parsing filesystem that doesn't have SCIF (0.0.52)
 - added fix that install routine happens in context of approot
 - files need to be added before running commands
 - fixed bug with appfiles copy command (0.0.51)
 - initial creation of just the scif client. (0.0.5)
