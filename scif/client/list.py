"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
import sys
import os


def main(args, parser, subparser):

    from scif.main import ScifRecipe

    client = ScifRecipe(writable=False, quiet=True)
    longlist = args.longlist

    result = []
    for app in client.apps():
        config = client.get_appenv(app)

        # Long listing includes a number with path to app
        if longlist is True:
            result.append([app.rjust(10), config["SCIF_APPROOT"]])
        else:
            result.append(app.rjust(10))

    if len(result) > 0:

        if longlist is True:
            header = "[app]              [root]"
            bot.custom(prefix="SCIF", message=header, color="CYAN")
            bot.table(result)
        else:
            print("\n".join(result))
