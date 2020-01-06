"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
import subprocess
import os
import re


# External Environment Functions


def append_path(self, varname, value):
    """append another directory to a path indexed by "varname" in the os.environ
       these variables are typically not represented by the user in the appenv,
       but are added dynamically by SCIF. Thus, they will appear in os.environ
       groups that are added to self.environment at runtime.

       Parameters
       ==========
       varname: the variable in the environment to append to (e.g., PATH)
       value: the path to append (no :)

    """
    value = self._append_path(varname, value)
    os.environ[varname] = value
    os.putenv(varname, value)


def get_append_path(self, key, value, environ=None):
    """the driver function of append_path, with intention to return the correct
       value and variable name for an environment of interest, this function
       maps to _append_path e.g.:
  
       1. if the variable is already defined, we append
       2. if the variable isn't defined, we set

       Parameters
       ==========
       key: the variable in the environment to append to (e.g., PATH)
       value: the path to append (no :)
       environment: the environment to look in.

    """
    from scif.defaults import SCIF_APPEND_PATHS, SCIF_ALLOW_APPEND

    if environ is None:
        environ = os.environ

    if key in environ and SCIF_ALLOW_APPEND and key in SCIF_APPEND_PATHS:
        return "%s:%s" % (value, os.environ[key])
    return value


def init_env(self, config, base="/scif", active=None):
    """ env will parse the complete SCIF namespace environment from a config.
        this will be defined for all apps to allow for easy interaction between
        them, regardless of which individual app is active.
    
        Parameters
        ==========
        config: the config loaded in with "load" in this file.
        active: the name of the active app, if relevant.

        Example: the following environment variables would be defined for an app
                 called "google-drive" Note that for the variable, the slash is
                 replaced with an underscore

             SCIF_APPDATA_google_drive=/scif/data/google-drive
             SCIF_APPRUN_google_drive=/scif/apps/google-drive/scif/runscript
             SCIF_APPHELP_google_drive=/scif/apps/google-drive/scif/runscript.help
             SCIF_APPROOT_google_drive=/scif/apps/google-drive
             SCIF_APPLIB_google_drive=/scif/apps/google-drive/lib
             SCIF_APPMETA_google_drive=/scif/apps/google-drive/scif
             SCIF_APPBIN_google_drive=/scif/apps/google-drive/bin
             SCIF_APPENV_google_drive=/scif/apps/google-drive/scif/environment.sh
             SCIF_APPLABELS_google_drive=/scif/apps/google-drive/scif/labels.json

        These paths and files are not created at this point, but just defined.

    """
    envars = dict()
    if "apps" in config:

        # Gloal SCIF variables for data and apps
        envars["SCIF_APPS"] = "%s/apps" % self._base
        envars["SCIF_DATA"] = "%s/data" % self._base

        for name, app in config["apps"].items():

            # Here we are adding variables for all apps.
            appenv = self.get_appenv_lookup(name)
            for varname, varval in appenv[name].items():
                updates = mk_env(key=varname, val=varval, app=name)
                envars.update(updates)

            # If this is the active app
            if active is not None:
                if active == name:
                    for varname, varval in appenv[name].items():
                        updates = mk_env(key=varname, val=varval)
                        envars.update(updates)

    return envars


def update_env(self, reset=False):
    """ If the SCIF is loaded, upload the object's environment.

        Parameters
        ==========
        reset: if True, empty the environment before parsing from config

    """

    if reset is True:
        self.environment = dict()

    if self._config is not None:

        # Update environment with app information
        updates = self._init_env(self._config, self._base)
        self.environment.update(updates)

    return self.environment


def mk_env(key, val, app=None):
    """a helper function to return a dictionary with a SCIF prefixed app name,
       the key slashes replaced with underscores, and the value set.

       Parameters
       ==========
       app: the app name to define the variable for (not used if not defined)
       key: the key (not including the SCIF_ prefix
       val: the value to set

    """
    key = "SCIF_%s" % key.upper()
    if app is not None:
        key = "%s_%s" % (key, app)

    key = re.sub("-|[.]", "_", key)
    return {key: val}


def load_env(self, app):
    """load an environment file for an app. We don't allow for manual entry
       of any file, but limit to predetermined environment.sh file, if exists.
       this function is inteded for runtime commands (shell or exec not install)

       Parameters
       ==========
       app: the app to export variables for

    """
    updates = dict()

    if app in self.apps():
        config = self.get_appenv(app)

        if "SCIF_APPENV" in config:
            envfile = config["SCIF_APPENV"]
            if os.path.exists(envfile):
                with open(envfile, "r") as filey:
                    lines = filey.readlines()
                for line in lines:
                    (key, _, val) = line.strip().partition("=")
                    if val not in ["", None]:  # skips export lines

                        updates[key] = val
                        self.environment[key] = val
    return updates


def export_env(self, ps1=True):
    """export the current environment, and add the PS1 variable to indicate
       the active shell display. This will start with values from the currently
       active environment, and then add those from scif.

       Parameters
       =========
       ps1: if True, change the shell prompt to scif>

    """

    runtime = os.environ.copy()

    if ps1 is True:
        runtime["PS1"] = "scif> "

    if hasattr(self, "environment"):

        # Step 1. Do an update, allowing extension for PATHs
        for key, val in self.environment.items():
            runtime[key] = self._append_path(key, val, self.environment)

        # Step 2; export
        for key, val in runtime.items():
            os.environ[key] = val
            os.putenv(key, val)

    return runtime


def get_appenv(self, app, isolated=True, update=False):
    """return environment for a specific app, meaning the variables active
       when it is running. 

       Parameters
       ==========
       isolated: if True, only return the active app variables (example  below)
       update: also update the global self.environment.

       If isolated is True, don't include other apps. For
       example, for an app `hello-world-echo` and isolated True, the following
       is returned:

       {
           'SCIF_APPBIN': '/scif/apps/hello-world-echo/bin',
           'SCIF_APPDATA': '/scif/data/hello-world-echo',
           'SCIF_APPENV': '/scif/apps/hello-world-echo/scif/environment.sh',
           'SCIF_APPHELP': '/scif/apps/hello-world-echo/scif/runscript.help',
           'SCIF_APPLABELS': '/scif/apps/hello-world-echo/scif/labels.json',
           'SCIF_APPLIB': '/scif/apps/hello-world-echo/lib',
           'SCIF_APPMETA': '/scif/apps/hello-world-echo/scif',
           'SCIF_APPNAME': 'hello-world-echo',
           'SCIF_APPRECIPE': '/scif/apps/hello-world-echo/scif/hello-world-echo.scif',
           'SCIF_APPROOT': '/scif/apps/hello-world-echo',
           'SCIF_APPRUN': '/scif/apps/hello-world-echo/scif/runscript'
           'SCIF_APPTEST': '/scif/apps/hello-world-echo/scif/test.sh'
       }

    """
    final = dict()
    if app in self.apps():
        environ = self.get_appenv_lookup(app)
        for var, val in environ[app].items():
            updates = mk_env(key=var, val=val)
            final.update(updates)

        # The user wants to include the current SCIF environment
        if isolated is False and hasattr(self, "environment"):
            final.update(self.environment)

        # The user also wants to update the SCIF environment
        if update is True:
            self.environment = final

        return final

    valid = " ".join(self.apps())
    bot.error("%s is not a valid app. Found %s" % (app, valid))


def get_appenv_lookup(self, app):
    """create a dictionary with a highest level index the
       app name, and underneath a generic lookup (without the app name) for
       different variable types.  

       Parameters
       ==========
       app: the new of the app to get the environment for
       isolated: if True don't include other apps

       Eg, app with name "google-drive" would look like:


       {'registry': {
                      'appbin': '/scif/apps/registry/bin',
                      'appdata': '/scif/data/registry',
                      'appenv': '/scif/apps/registry/scif/environment.sh',
                      'apphelp': '/scif/apps/registry/scif/runscript.help',
                      'apptest': '/scif/apps/registry/scif/test.sh',
                      'applabels': '/scif/apps/registry/scif/labels.json',
                      'applib': '/scif/apps/registry/lib',
                      'appmeta': '/scif/apps/registry/scif',
                      'apprecipe': '/scif/apps/registry/scif/registry.scif'
                      'approot': '/scif/apps/registry',
                      'apprun': '/scif/apps/registry/scif/runscript'
                    }            
       }

       This function is intended to be shared by env above and the environment
       generating functions in the main client, to have consistent behavior. 
       The above data structure gets parse into the (global) variables for
       the particular app:

       {'SCIF_APPBIN_registry': '/scif/apps/registry/bin',
        'SCIF_APPDATA_registry': '/scif/data/registry',
        'SCIF_APPENV_registry': '/scif/apps/registry/scif/environment.sh',
        'SCIF_APPHELP_registry': '/scif/apps/registry/scif/runscript.help',
        'SCIF_APPLABELS_registry': '/scif/apps/registry/scif/labels.json',
        'SCIF_APPTEST_registry': '/scif/apps/registry/scif/test.sh',
        'SCIF_APPLIB_registry': '/scif/apps/registry/lib',
        'SCIF_APPMETA_registry': '/scif/apps/registry/scif',
        'SCIF_APPRECIPE_registry': '/scif/apps/registry/scif/registry.scif',
        'SCIF_APPROOT_registry': '/scif/apps/registry',
        'SCIF_APPRUN_registry': '/scif/apps/registry/scif/runscript'}

    """

    if app in self.apps():

        base = self._base
        envars = {app: {}}

        # Roots for app data and app files
        appdata = "%s/data/%s" % (base, app)
        approot = "%s/apps/%s" % (base, app)
        appmeta = "%s/scif" % (approot)

        envars[app]["appdata"] = appdata
        envars[app]["approot"] = approot
        envars[app]["appmeta"] = appmeta

        envars[app]["appbin"] = "%s/bin" % (approot)
        envars[app]["applib"] = "%s/lib" % (approot)
        envars[app]["apprun"] = "%s/runscript" % (appmeta)
        envars[app]["apphelp"] = "%s/runscript.help" % (appmeta)
        envars[app]["appenv"] = "%s/environment.sh" % (appmeta)
        envars[app]["apptest"] = "%s/test.sh" % (appmeta)
        envars[app]["applabels"] = "%s/labels.json" % (appmeta)
        envars[app]["apprecipe"] = "%s/%s.scif" % (appmeta, app)
        envars[app]["appname"] = app
        return envars

    # if we get down here, didn't have the app in the first place
    valid = " ".join(self.apps())
    bot.error("%s is not a valid app. Found %s" % (app, valid))


# ScifRecipe Environment Helpers


def add_env(self, key, value):
    """ add a key/value pair to the environment. Should begin with SCIF
        to maintain proper namespace

        Parameters
        ==========
        key: the environment variable name. For SCIF, slashes should be 
             removed and replaced with underscore.
        value: the value to set for the environment variable

    """
    if not hasattr(self, "environment"):
        self.environment = dict()

    if not key.startswith("SCIF"):
        msg = "Environment variable outside SCIF namespace not recommended."
        bot.warning(msg)

    # If the variable already exists, status is "update"
    action = "new"
    if key in self.environment:
        action = "update"

    self.environment[key] = value
    bot.debug("[environment:%s][%s=%s]" % (action, key, value))


def get_env(self, key=None):
    """return a particular value for an environment variable, if the key
       exists. If no keys are defined, the entire environment is returned.
       For an app-specific environment, use get_appenv.
    """
    if key is not None:
        if key in self.environment:
            bot.info(self.environment[key])
            return self.environment[key]

    # otherwise, return the entire environment lookup
    if hasattr(self, "environment"):
        return self.environment
