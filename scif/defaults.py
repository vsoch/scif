"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
import tempfile
import os
import pwd

################################################################################
# environment / options
################################################################################


def convert2boolean(arg):
    """
    convert2boolean is used for environmental variables
    that must be returned as boolean
    """
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    """ getenv will attempt to get an environment variable. If the variable
        is not found, None is returned.

        Paramters
        =========
        variable_key: the variable name
        required: exit with error if not found
        silent: Do not print debugging information for variable
    """
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.exit("Cannot find environment variable %s, exiting." % variable_key)

    if not silent and variable is not None:
        bot.verbose("%s found as %s" % (variable_key, variable))

    return variable


def getenv_namespace(namespace="SCIF", func=None):
    """return all environment variables in a particular namespace, such as for
       SCIF apps using a filter function (func). The function should take first
       a key in the environment, and then the namespace variable. 
       If none provided, uses "starts with" equivalent.

        def func(key, namespace):
            return key.startswith(namespace)
    """
    if func is None:
        """does key start with namespace?"""

        def func(key, namespace):
            return key.startswith(namespace)

    env = os.environ.items()
    return [{key: value} for key, value in env if func(key, namespace)]


################################################################################
# Defaults


# Supported Sections
sections = (
    "appenv",
    "applabels",
    "appinstall",
    "appfiles",
    "apphelp",
    "apprun",
    "apptest",
)


################################################################################
# Scientific Filesystem (environment)


#########################
# Global Settings
#########################

SCIF_APPS = getenv_namespace(namespace="SCIF_APP")
SCIF_BASE = getenv("SCIF_BASE", "/scif")
SCIF_DATA = getenv("SCIF_DATA", "%s/data" % SCIF_BASE)
SCIF_APPS = getenv("SCIF_APPS", "%s/apps" % SCIF_BASE)
SCIF_PYSHELL = getenv("SCIF_PYSHELL", "ipython")
SCIF_SHELL = getenv("SCIF_SHELL", "/bin/bash")
SCIF_ENTRYPOINT = getenv("SCIF_ENTRYPOINT", "/bin/bash")
SCIF_ENTRYFOLDER = getenv("SCIF_ENTRYFOLDER")  # default None, is set to /scif
# in functions OR app roots

#########################
# Permissions
#########################

SCIF_APPEND_PATHS = ["PYTHONPATH", "PATH", "LD_LIBRARY_PATH"]
SCIF_ALLOW_APPEND = convert2boolean(getenv("SCIF_ALLOW_APPEND", True))
