"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from collections import OrderedDict
from scif.logger import bot
from scif.utils import read_file
from scif.defaults import sections
import os
import re


def load_filesystem(base, quiet=False):
    """load a filesystem based on a root path, which is usually /scif

        Parameters
        ==========
        base: base to load.

        Returns
        =======
        config: a parsed recipe configuration for SCIF
    """
    from scif.defaults import SCIF_APPS

    if os.path.exists(SCIF_APPS):
        apps = os.listdir(SCIF_APPS)
        config = {"apps": {}}
        for app in apps:
            path = "%s/%s/scif/%s.scif" % (SCIF_APPS, app, app)
            if os.path.exists(path):
                recipe = load_recipe(path)
                config["apps"][app] = recipe["apps"][app]

        if len(config["apps"]) > 0:
            if quiet is False:
                bot.info("Found configurations for %s scif apps" % len(config["apps"]))
                bot.info("\n".join(list(config["apps"].keys())))
            return config


def load_recipe(path):
    """load will return a loaded in (user) scif configuration file

        Parameters
        ==========
        path: a path to a scif recipe file

        Returns
        =======
        config: a parsed recipe configuration for SCIF
    """

    path = os.path.abspath(path)
    if os.path.exists(path):

        # Read in spec, skip empty lines, don't strip remaining
        spec = [
            x.strip("\n")
            for x in read_file(path)
            if not re.match(r"^\s+$", x.strip("\n"))
        ]

        spec = [x for x in spec if x not in ["", None]]
        config = OrderedDict()
        section = None
        name = None

        while len(spec) > 0:

            # Clean up white trailing/leading space
            line = spec.pop(0)
            stripped = line.strip()

            # Comment
            if stripped.startswith("#"):
                continue

            # A new section?
            elif stripped.startswith("%"):

                # Remove any comments
                line = line.split("#", 1)[0].strip()

                # Is there a section name?
                parts = line.split(" ")
                if len(parts) > 1:
                    name = " ".join(parts[1:])
                section = re.sub(r"[%]|(\s+)", "", parts[0]).lower()
                config = add_section(config=config, section=section, name=name)

            # If we have a section, and are adding it
            elif section is not None:
                spec = [line] + spec
                config = read_section(
                    config=config, spec=spec, section=section, name=name
                )

        # Make sure app environments are sourced as first line of recipe
        config = finish_recipe(config)

    else:
        bot.debug("Cannot find recipe file %s" % path)
    return config


def finish_recipe(config, global_section="apps"):
    """
       finish recipe includes final steps to add to the runtime for an app.
       Currently, this just means adding a command to source an environment
       before running, if appenv is defined. The Python should handle putting
       variables in the environment, however in some cases (if the variable
       includes an environment variable:

          VARIABLE1=$VARIABLE2

       It would not be properly sourced! So we add a source as the first
       line of the runscript

       Parameters
       ==========
       config: the configuation file produced by load_recipe. Assumed to have
               a highest key of "apps" and then lookup by individual apps,
               and then sections. Eg: config['apps']['myapp']['apprun'] 

    """
    # The apps are the keys under global section "apps"
    apps = list(config[global_section].keys())

    for app in apps:

        # If an apprun is present and the system supports source, do it.
        if "appenv" in config[global_section][app]:
            appenv = config[global_section][app]["appenv"]

            # If runscript or test is defined, add source to first line
            if "apptest" in config[global_section][app]:
                apptest = config[global_section][app]["apptest"]
                config[global_section][app]["apptest"] = appenv + apptest

            if "apprun" in config[global_section][app]:
                apprun = config[global_section][app]["apprun"]
                config[global_section][app]["apprun"] = appenv + apprun

    return config


def read_section(config, spec, section, name, global_section="apps"):
    """read in a section to a list, and stop when we hit the next section
    """
    members = []

    while True:

        if len(spec) == 0:
            break
        next_line = spec[0]

        if next_line.upper().strip().startswith("%"):
            break
        else:
            new_member = spec.pop(0)
            if not new_member.strip().startswith("#"):

                # Strip whitespace for labels, files, environment
                if section in ["applabels", "appfiles", "appenv"]:
                    new_member = new_member.strip()

                members.append(new_member)

    # Add the list to the config
    if len(members) > 0:
        if section is not None and name is not None:
            config[global_section][name][section] = members
        else:  # section is None, is just global
            config[global_section] = members

    return config


def add_section(config, section, name=None, global_section="apps"):
    """ add section will add a section (and optionally)
        section name to a config

        Parameters
        ==========
        config: the config (dict) parsed thus far
        section: the section type (e.g., appinstall)
        name: an optional name, added as a level (e.g., google-drive)

        Resulting data structure is:

            config['registry']['apprun']
            config[name][section]

    """

    if section is None:
        bot.exit("You must define a section (e.g. %appenv) before any action.")

    if section not in sections:
        bot.exit("%s is not a valid section." % section)

    # Add the global section, if doesn't exist
    if global_section not in config:
        config[global_section] = OrderedDict()

    if name is not None:
        if name not in config[global_section]:
            config[global_section][name] = OrderedDict()

        if section not in config[global_section][name]:
            config[global_section][name][section] = []
            bot.debug("Adding section %s %s" % (name, section))

    return config
