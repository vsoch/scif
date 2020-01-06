"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from scif.main.helpers import parse_entrypoint
from scif.defaults import SCIF_ENTRYFOLDER, SCIF_SHELL
import sys
import os


def app(self, app):
    """view a single app, if it exists

    Parameters
    ==========
    app: the name of the app to view
        """
    if "apps" in self._config:
        if app in self._config["apps"]:
            return self._config["apps"][app]


def apps(self):
    """get a list of apps to show the user
    """
    apps = []
    if self._config is not None:
        if "apps" in self._config:
            apps = list(self._config["apps"])
    return apps


def activate(self, app, cmd=None, args=None):
    """if an app is valid, get it's environment to make it active.
       Update the entrypoint to be relevant to the app runscript.
    
        Parameters
        ==========
        app: the name of the app to activate
        cmd: if defined, the entry point (command) to run. Otherwise uses apprun
        args: additional commands for the apprun

    """
    if app is None:
        bot.warning("No app selected, will run default %s" % self._entry_point)
        self.reset()

    elif app in self.apps():
        config = self.get_appenv(app)

        # Make app active
        self._active = app

        # Make sure bin is added to path, and lib to ld_library_path
        self.append_path("PATH", config["SCIF_APPBIN"])
        self.append_path("LD_LIBRARY_PATH", config["SCIF_APPLIB"])

        # Set the runscript, first to cmd provided (exec) then runscript
        if cmd != None:
            self._entry_point = parse_entrypoint(cmd)
            if args is not None:
                self._entry_point += parse_entrypoint(args)
        else:
            # Set the default entrypoint
            self._set_entrypoint(app, "SCIF_APPRUN", args)

        # Update the environment for active app (updates ScifRecipe object)
        appenv = self.get_appenv(app, isolated=False, update=True)

        self.load_env(app)  # load environment variables from app itself
        self.export_env()  # export all variables from client.environment

        # Only set entryfolder if user didn't set to something else
        if not SCIF_ENTRYFOLDER:
            self._entry_folder = appenv["SCIF_APPROOT"]

    else:
        bot.warning("%s is not an installed SCIF app" % app)


def deactivate(self, app):
    """if an app is valid, change the state so the app is no longer active.
       This is currently equivalent to calling reset, but only doing so if the
       app is defined for the SCIF.

    Parameters
    ==========
    app: the name of the app to deactivate
    """

    if app in self.apps():
        self.reset()

    else:
        bot.warning("%s is not an installed SCIF app" % app)


def help(self, app):
    """print the help file for an app, if it exists.

       Parameters
       ==========
       app: the app to export variables for

    """
    lines = None
    if app in self.apps():
        config = self.get_appenv(app)

        if "SCIF_APPHELP" in config:
            helpfile = config["SCIF_APPHELP"]
            if os.path.exists(helpfile):
                with open(helpfile, "r") as filey:
                    lines = filey.readlines()
                print("".join(lines))

    if lines is None:
        bot.info("No help is defined for %s" % app)
    return lines


def reset(self):
    """reset the SCIF filesystem, meaning that defaults are set, the entrypoint
      if reset, and the environment is reset. Only maintain entry folder set
      by environment, if it was defined.
    """

    self.set_defaults()
    # Make the active app None
    # self._active = None
    # Update the entry point to use default
    # self._entry_point = parse_entrypoint()

    # Reset the environment
    self.update_env(reset=True)

    # set entry folder back to use preference, if original is not None
    if not SCIF_ENTRYFOLDER:
        self._entry_folder = SCIF_ENTRYFOLDER


def inspect(self, app, attributes=None):
    """inspect an app based on a list of attributes to inspect.

    Parameters
    ==========
    app: the name of the app to inspect
    attributes: a list of attributes to return
    """
    result = {}
    if app not in self.apps():
        return result

    if attributes is None:
        attributes = ["all"]

    lookup = self.app(app)

    if "a" in attributes or "all" in attributes:
        return lookup

    if "h" in attributes or "help" in attributes and "apphelp" in lookup:
        result["apphelp"] = lookup["apphelp"]
    if "f" in attributes or "files" in attributes and "appfiles" in lookup:
        result["appfiles"] = lookup["appfiles"]
    if "r" in attributes or "runscript" in attributes and "apprun" in lookup:
        result["apprun"] = lookup["apprun"]
    if "t" in attributes or "test" in attributes and "apptest" in lookup:
        result["apptest"] = lookup["apptest"]
    if "l" in attributes or "labels" in attributes and "applabels" in lookup:
        result["applabels"] = lookup["applabels"]
    if "e" in attributes or "environment" in attributes and "appenv" in lookup:
        result["appenv"] = lookup["appenv"]
    if "i" in attributes or "install" in attributes and "appinstall" in lookup:
        result["appinstall"] = lookup["appinstall"]

    return result
