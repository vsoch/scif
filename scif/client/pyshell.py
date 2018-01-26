'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2018 Vanessa Sochat.

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
import os


def main(args,parser,subparser):

    from scif.defaults import SCIF_SHELL as shell

    parsed = parse_input_preferences(args.recipe, 
                                     quiet=args.quiet)

    recipe = parsed['recipe']
    quiet = parsed['quiet']
    app = parsed['app']

    # The client will either load the recipe or the base

    lookup = { 'ipython': ipython,
               'python': python,
               'bpython': bpython }

    shells = ['ipython', 'python', 'bpython']

    # If the user asked for a specific shell via environment
    if shell is not None:
        shell = shell.lower()
        if shell in lookup:
            try:    
                return lookup[shell](recipe=recipe, 
                                     app=app, 
                                     quiet=quiet,
                                     writable=args.writable)
            except ImportError:
                pass

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](recipe=recipe, 
                                 app=app, 
                                 quiet=quiet,
                                 writable=args.writable)
        except ImportError:
            pass
    

def ipython(recipe, app=None, quiet=False, writable=True):
    '''embed the client with loaded recipe into an ipython session
    '''
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
    bpython.embed(locals_={'client': client})

def python(recipe, app=None, quiet=False, writable=True):
    from scif.main import ScifRecipe
    import code
    client = ScifRecipe(recipe, quiet=quiet, writable=writable)
    client.speak()
    if app is not None:
        client.activate(app)
    code.interact(local={"client":client})
