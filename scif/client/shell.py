"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.logger import bot
from scif.defaults import SCIF_SHELL, SCIF_BASE
import sys
import pwd
import os


def main(args, parser, subparser):

    from scif.main import ScifRecipe

    app = args.app
    client = ScifRecipe(quiet=True, writable=args.writable)

    # Only allow interactive shell if the base exists
    if os.path.exists(SCIF_BASE):
        client.shell(app, cmd=[SCIF_SHELL])
