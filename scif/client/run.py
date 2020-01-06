"""

Copyright (C) 2016-2020 Vanessa Sochat.

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

    cmd = args.cmd

    if len(cmd) == 0:
        bot.warning("You must supply an appname to run.")
        bot.custom(prefix="Example: ", message="scif run <app>")
        sys.exit(1)

    app = cmd.pop(0)

    # Remaining arguments indicate options/args to pass on
    if len(cmd) == 0:
        cmd = None

    client = ScifRecipe(quiet=True, writable=args.writable)
    client.run(app, args=cmd)
