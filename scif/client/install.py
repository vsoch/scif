"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
import pwd
import os


def main(args, parser, subparser):

    from scif.main import ScifRecipe

    apps = args.recipe

    if len(apps) == 0:
        bot.exit("You must provide a recipe (.scif) file to install.")

    recipe = apps.pop(0)

    if not os.path.exists(recipe):
        bot.exit("Cannot find recipe file %s" % recipe)

    if len(apps) == 0:
        apps = None

    client = ScifRecipe(path=recipe)  # writable is True

    # Preview the entire recipe, or the apps chosen
    client.install(apps)
