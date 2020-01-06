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
import os


def main(args, parser, subparser):

    from scif.defaults import SCIF_SHELL as shell

    parsed = parse_input_preferences(args.recipe, quiet=args.quiet)

    recipe = parsed["recipe"]
    quiet = parsed["quiet"]
    app = parsed["app"]

    # The client will either load the recipe or the base

    lookup = {"ipython": ipython, "python": python, "bpython": bpython}

    shells = ["ipython", "python", "bpython"]

    # If the user asked for a specific shell via environment
    if shell is not None:
        shell = shell.lower()
        if shell in lookup:
            try:
                return lookup[shell](
                    recipe=recipe, app=app, quiet=quiet, writable=args.writable
                )
            except ImportError:
                pass

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](
                recipe=recipe, app=app, quiet=quiet, writable=args.writable
            )
        except ImportError:
            pass


def ipython(recipe, app=None, quiet=False, writable=True):
    """embed the client with loaded recipe into an ipython session
    """
    from scif.main import ScifRecipe
    from IPython import embed

    client = ScifRecipe(recipe, quiet=quiet, writable=writable)
    client.speak()
    if app is not None:
        client.activate(app)
    embed()


def bpython(recipe, app=None, quiet=False, writable=True):
    from scif.main import ScifRecipe
    import bpython

    client = ScifRecipe(recipe, quiet=quiet, writable=writable)
    client.speak()
    if app is not None:
        client.activate(app)
    bpython.embed(locals_={"client": client})


def python(recipe, app=None, quiet=False, writable=True):
    from scif.main import ScifRecipe
    import code

    client = ScifRecipe(recipe, quiet=quiet, writable=writable)
    client.speak()
    if app is not None:
        client.activate(app)
    code.interact(local={"client": client})
