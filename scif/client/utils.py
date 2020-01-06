"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from scif.defaults import SCIF_BASE


import sys
import os


def parse_input_preferences(recipe, quiet=False):
    """parse a recipe|app, meaning a list of one or more things that could be

       any of the following:

        Returns
        =======
        parsed: a dictionary lookup with keys for app, recipe, and quiet.
    """

    # if coming from inspect, will be string
    if not isinstance(recipe, list):
        recipe = [recipe]

    # First case: recipe and app
    if len(recipe) > 1:

        app = recipe[1]
        recipe = recipe[0]
        quiet = True

    # Second case, no input or recipe|app
    else:

        app = None

        # If no recipe provided, assume loading base

        if len(recipe) == 0:
            recipe = SCIF_BASE

        # Otherwise, we need to figure out if recipe or base
        else:
            recipe = recipe[0]

            # If recipe doesn't exist as a file, assume it's an app
            if not os.path.exists(recipe):
                app = recipe
                recipe = SCIF_BASE

            # If the recipe provided is a file, no app detection
            else:
                quiet = True

    # Return the parsed data structure
    parsed = {"quiet": quiet, "app": app, "recipe": recipe}

    return parsed
