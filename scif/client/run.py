'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

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

import sys
import pwd
import os

def main(args,parser,subparser):

    from scif.main import ScifRecipe
    cmd = args.app
    client = ScifRecipe(quiet=True, writable=args.writable)

    # If command is set to an app (or more), otherwise we default to /bin/bash
    app = None
    if cmd is not None:
        if not instance(cmd,list):
            cmd = [cmd]

        # The app is the first argument 
        app = cmd.pop(0)

        # Additional commands to pass into run, or set to None
        if len(cmd) == 0:
            cmd = None

    client = ScifRecipe(quiet=True, writable=args.writable)
    client.run(app, args=cmd)
