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
from scif.defaults import SCIF_SHELL, SCIF_BASE
import sys
import pwd
import os

    
def main(args,parser,subparser):

    from scif.main import ScifRecipe
    app = args.app
    client = ScifRecipe(quiet=True, writable=args.writable)

    # Only allow interactive shell if the base exists
    if os.path.exists(SCIF_BASE):
        client.shell(app, cmd=[SCIF_SHELL])
