"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from datetime import datetime
from scif.utils import mkdir_p, write_file, write_json
from scif.main.helpers import get_parts
import os


def preview(self, apps=None):
    """preview the complete setup for a scientific filesytem. This is useful 
       to print out actions for install (without doing them).
    """
    self._preview_base()  # preview the folder structure
    self._preview_apps(apps)  # App install


def preview_base(self):
    """ preview basic scif structure at the base for apps and metadata

        Parameters
        ==========
        base: the full path to the root folder to create /scif
    """
    if not hasattr(self, "_base"):
        bot.exit("Please set the base before preview.")

    bot.custom(prefix="[base] %s" % self._base, color="CYAN")
    bot.custom(prefix="[apps] %s" % self.path_apps, color="CYAN")
    bot.custom(prefix="[data] %s\n" % self.path_data, color="CYAN")


def preview_apps(self, apps=None):
    """install one or more apps to the base. If app is defined, only
       install app specified. Otherwise, install all found in config.
    """
    if apps in [None, []]:
        apps = self.apps()

    if not isinstance(apps, list):
        apps = [apps]

    for app in apps:

        # We must have the app defined in the config
        if app not in self._config["apps"]:
            bot.exit("Cannot find app %s in config." % app)

        # Make directories
        bot.newline()
        settings = self._init_app_preview(app)

        # Get the app configuration
        config = self.app(app)

        # Handle environment, runscript, labels
        self._preview_runscript(app, settings, config)
        self._preview_environment(app, settings, config)
        self._preview_labels(app, settings, config)
        self._preview_commands(app, settings, config)
        self._preview_files(app, settings, config)
        self._preview_recipe(app, settings, config)
        self._preview_test(app, settings, config)
        bot.newline()


def init_app_preview(self, app):
    """initialize an app, meaning adding the metadata folder, bin, and 
       lib to it. The app is created at the base
    """
    settings = self.get_appenv_lookup(app)[app]

    for key in ["root", "lib", "bin", "data"]:
        val = settings["app%s" % key]
        bot.custom(prefix="[%s] %s" % (key, val), color="CYAN")

    return settings


def preview_runscript(self, app, settings, config):
    """preview the runscript for an app
       
       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """
    if "apprun" in config:
        content = "\n".join(config["apprun"])
        bot.info("+ " + "apprun ".ljust(5) + app)
        print(settings["apprun"])
        print(settings["apphelp"])
        print(content)


def preview_test(self, app, settings, config):
    """preview the test for the app

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """
    if "apptest" in config:
        content = "\n".join(config["apptest"])
        bot.info("+ " + "apptest ".ljust(5) + app)
        print(settings["apptest"])
        print(content)


def preview_labels(self, app, settings, config):
    """preview labels for an app

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """
    lookup = ""
    if "applabels" in config:
        labels = config["applabels"]
        bot.info("+ " + "applabels ".ljust(5) + app)
        print(settings["applabels"])
        for line in labels:
            label, value = get_parts(line, default="")
            lookup += "%s=%s\n" % (label, value)
        print(lookup)
    return lookup


def preview_files(self, app, settings, config):
    """install files will add files (or directories) to a destination.
       If none specified, they are placed in the app base

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """

    if "appfiles" in config:
        files = config["appfiles"]
        bot.info("+ " + "appfiles ".ljust(5) + app)

        for pair in files:

            # Step 1: determine source and destination
            src, dest = get_parts(pair, default=settings["approot"])
            print("%s --> %s \n" % (src, dest))


def preview_commands(self, app, settings, config):
    """install will finally, issue commands to install the app.

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """
    cmd = ""
    if "appinstall" in config:
        cmd = config["appinstall"]
        bot.info("+ " + "appinstall ".ljust(5) + app)
        print("\n".join(cmd))
    return cmd


def preview_recipe(self, app, settings, config):
    """Write the initial recipe for the app to its metadata folder.

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars
       config: should be the config for the app obtained with self.app(app)

    """
    recipe_file = settings["apprecipe"]
    recipe = "# [scif] scientific filesystem recipe\n"
    recipe += "# [date] %s\n" % datetime.now().strftime("%b-%d-%Y")
    bot.info("+ " + "apprecipe ".ljust(5) + app)
    print(recipe_file)

    for section_name, section_content in config.items():
        content = "%s\n" % "\n".join(section_content)
        header = "%" + section_name + " %s" % app
        recipe += "%s\n%s\n" % (header, content)

    return recipe


def preview_environment(self, app, settings, config):
    """preview the environment section

       Parameters
       ==========
       app should be the name of the app, for lookup in config['apps']
       settings: the output of _init_app(), a dictionary of environment vars

    """
    content = ""
    if "appenv" in config:
        content = "\n".join(config["appenv"])
        bot.info("+ " + "appenv ".ljust(5) + app)
        print(settings["appenv"])
        print(content)
    return content
