'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

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

from scif.logger import bot
import sys
import pwd
import os

    

def main(args,parser,subparser):

    from scif.main import ScifRecipe
    cmd = args.cmd

    if len(cmd) < 2:
        bot.warning('You must supply an appname and command to execute.')
        bot.custom(prefix="Example: ", message="scif exec app echo $SCIF_APPNAME")
        sys.exit(1)

    app = cmd.pop(0)
    client = ScifRecipe(quiet=True, writable=args.writable)
    client.execute(app, cmd)
