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

    client = ScifRecipe(quiet=True, writable=False)
    apps = client.apps()

    for app in apps:
        inspection = client.inspect(app)
        if len(inspection) > 0:
            for key, val in inspection.items():
                print("%" + key)
                print("\n".join(val) + "\n")
