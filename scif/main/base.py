"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from scif.main.parser import load_filesystem, load_recipe
import os
import sys

bot.level = 3


class ScifRecipe:
    """Create and work with a scif recipe. Usage typically looks like:

       recipe = ScifRecipe('sregistry.scif')
       
       Parameters
       ==========
       path: the path to the scif recipe flie.

    """

    def __init__(self, path=None, app=None, writable=True, quiet=False):
        """initialize the scientific filesystem by creating a scif folder
           at the base, and loading the recipe to fill it.

           Parameters
           ==========
           path: is the first paramter, not required to initialize an empty 
                 client session. The logic proceeds as follows:
                 1. If path is not defined, we want (empty) interactive session
                 2. We derive the base from the environment SCIF_BASE
        """

        # 0. base determined from environment
        from scif.defaults import SCIF_BASE

        self.set_defaults()
        self.quiet = quiet

        # If recipe path not provided, try default base
        if path is None:
            path = SCIF_BASE

        # 1. Determine if path is a recipe or base
        if path is not None:

            self.set_base(SCIF_BASE, writable=writable)  # /scif
            self.load(path, app, quiet)  # recipe, environment

        # 2. Neither, development client
        else:
            bot.info("[skeleton] session!")
            bot.info('           load a recipe: client.load("recipe.scif")')
            bot.info('           change default base:  client.set_base("/")')

    def __str__(self):
        return "[scif]"

    def __repr__(self):
        return "[scif]"

    def speak(self):
        """the client should announce self given that the shell is being used.
        """
        if self._base is not None:
            apps = " | ".join(self.apps())
            bot.custom(prefix="%s %s" % (self, self._base), message=apps, color="CYAN")
        else:
            bot.info(self)

    def load(self, path, app=None, quiet=False):
        """load a scif recipe into the object

            Parameters
            ==========
            path: the complete path to the config (recipe file) to load, or 
                  root path of filesystem (that from calling function defaults to
                  /scif)
            app:  if running with context of an active app, this will load the
                  active app environment for it as well.
        """
        # 1. path is a recipe
        if os.path.isfile(path):
            self._config = load_recipe(path)

        # 2. path is a base
        elif os.path.isdir(path):
            self._config = load_filesystem(path, quiet=quiet)

        else:
            bot.warning("%s is not detected as a recipe or base." % path)
            self._config = None

        self.update_env(app)
