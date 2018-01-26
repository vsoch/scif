'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from scif.logger import bot
from scif.defaults import SCIF_BASE


import sys
import os


def parse_input_preferences(recipe, quiet=False):
    '''parse a recipe|app, meaning a list of one or more things that could be

       any of the following:

        Returns
        =======
        parsed: a dictionary lookup with keys for app, recipe, and quiet.
    '''

    # if coming from inspect, will be string
    if not isinstance(recipe,list):
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
    parsed = {'quiet': quiet,
              'app': app,
              'recipe': recipe }

    return parsed
