"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
import sys
import pwd
import os


def main(args, parser, subparser):

    from scif.main import ScifRecipe

    apps = args.app
    client = ScifRecipe(quiet=True, writable=False)

    if len(apps) == 0:
        bot.info("Usage: scif help <hello-world>")
    for app in apps:
        client.help(app)
