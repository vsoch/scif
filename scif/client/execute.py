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

    cmd = args.cmd

    if len(cmd) < 2:
        bot.warning("You must supply an appname and command to execute.")
        bot.custom(prefix="Example: ", message="scif exec app echo $SCIF_APPNAME")
        sys.exit(1)

    app = cmd.pop(0)

    # The next must be the program to execute
    command = cmd.pop(0)

    client = ScifRecipe(quiet=True, writable=args.writable)
    client.execute(app=app, cmd=command, args=cmd)
