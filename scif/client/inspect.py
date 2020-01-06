"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.client.utils import parse_input_preferences
from scif.logger import bot
import sys
import json
import os


def main(args, parser, subparser):

    from scif.main import ScifRecipe

    # Inspect choices, r, e, l, a
    choices = [
        "r",
        "e",
        "l",
        "a",
        "f",
        "i",
        "h",
        "dump",
        "labels",
        "all",
        "files",
        "help",
        "install",
        "environment",
        "definition",
        "runscript",
    ]

    attributes = [x for x in args.attributes if x in choices]

    write_recipe = False
    if "dump" in attributes:
        write_recipe = True
        attributes.pop(attributes.index("dump"))

    apps = [x for x in args.attributes if x not in attributes]

    # First instantiate the client
    client = ScifRecipe(quiet=True, writable=False)

    # Filter down to apps that we want
    if len(apps) == 0:
        apps = client.apps()

    if len(attributes) == 0:
        attributes = ["a"]

    result = {}
    for app in apps:

        inspection = client.inspect(app, attributes)
        if len(inspection) > 0:
            result[app] = inspection

    if write_recipe is True:
        for app, atts in result.items():
            for key, val in atts.items():
                print("%" + key)
                print("\n".join(val) + "\n")
    else:
        print(json.dumps(result, indent=4, separators=(",", ": ")))
