"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from scif.utils import mkdir_p
from scif.main.helpers import parse_entrypoint
import os


def set_base(self, base="/", writable=True):
    """ set the base (the root where to create /scif) and determine if
        it is writable

        Parameters
        ==========
        base: the full path to the root folder to create /scif
    """
    # The user is likely to give path to scif (should still work)
    base = base.strip("scif")

    if not os.path.exists(base):
        bot.exit("%s does not exist!" % base)

    base = "/%s" % os.path.abspath(base).strip("/")
    self._base = os.path.join(base, "scif")
    self.path_apps = "%s/apps" % self._base
    self.path_data = "%s/data" % self._base

    # Update the environment
    self.add_env("SCIF_DATA", self.path_data)
    self.add_env("SCIF_APPS", self.path_apps)

    # Check if it's writable
    if writable is True:
        if not os.access(base, os.W_OK):
            bot.exit("%s is not writable." % base)


def set_defaults(self, entry_point=None):
    """set the defaults for the SCIF state at start up. 
       Usually this means parsing them from the environment. We hold these
       with the object so we can easily maintain and change state.
    """

    # The entrypoint is the runscript (or /bin/bash default)
    self._entry_point = parse_entrypoint(entry_point)

    # Set the default entry folder, changed to app if in context of app
    from scif.defaults import SCIF_ENTRYFOLDER

    self._entry_folder = SCIF_ENTRYFOLDER  # Defaults to None

    # The active app, coinciding with the entry_point
    self._active = None


def install_base(self):
    """ create basic scif structure at the base for apps and metadata

        Parameters
        ==========
        base: the full path to the root folder to create /scif
    """
    if not hasattr(self, "_base"):
        bot.exit("Please set the base before installing to it.")

    bot.info("Installing base at %s" % self._base)

    mkdir_p(self.path_apps)
    mkdir_p(self.path_data)
