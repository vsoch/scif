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
import os

    

def main(args,parser,subparser):

    from scif.main import ScifRecipe
    client = ScifRecipe(writable=False, quiet=True)
    longlist = args.longlist
    
    result = []
    for app in client.apps():
        config = client.get_appenv(app)

        # Long listing includes a number with path to app
        if longlist is True:
            result.append([app.rjust(10), config['SCIF_APPROOT']]) 
        else:
            result.append(app.rjust(10))

    if len(result) > 0:

        if longlist is True:
            header = "[app]              [root]"
            bot.custom(prefix="SCIF", message=header, color="CYAN")
            bot.table(result)
        else:
            print('\n'.join(result))
