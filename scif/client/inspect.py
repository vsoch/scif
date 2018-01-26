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

from scif.client.utils import parse_input_preferences
from scif.logger import bot
import sys
import json
import os


def main(args,parser,subparser):

    from scif.main import ScifRecipe

    # Inspect choices, r, e, l, a
    choices = ['r', 'e', 'l', 'a', 'f', 'i', 'h', 'dump',
               'labels', 'all', 'files', "help", "install",
               'environment', 'definition', 'runscript'] 

    attributes = [x for x in args.attributes if x in choices]

    write_recipe = False
    if "dump" in attributes:
        write_recipe = True
        attributes.pop(attributes.index('dump'))

    apps = [x for x in args.attributes if x not in attributes]
    
    # First instantiate the client
    client = ScifRecipe(quiet=True, writable=False)

    # Filter down to apps that we want
    if len(apps) == 0:
        apps = client.apps()

    if len(attributes) == 0:
        attributes = ['a']

    result = {}
    for app in apps:

        inspection = client.inspect(app, attributes)
        if len(inspection) > 0:
            result[app] = inspection 

    if write_recipe is True:
        for app, atts in result.items():
            for key,val in atts.items():
                print('%' + key)
                print('\n'.join(val) + '\n')
    else:
        print(json.dumps(result,
                         indent=4,
                         separators=(',', ': ')))
