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
from scif.utils import mkdir_p
from scif.main.helpers import parse_entrypoint
import sys
import os


def set_base(self, base='/', writable=True):
    ''' set the base (the root where to create /scif) and determine if
        it is writable

        Parameters
        ==========
        base: the full path to the root folder to create /scif
    '''
    # The user is likely to give path to scif (should still work)
    base = base.strip('scif')

    if not os.path.exists(base):
        bot.error('%s does not exist!' %base)
        sys.exit(1)

    base = "/%s" %os.path.abspath(base).strip('/')
    self._base = os.path.join(base,'scif')
    self.path_apps = '%s/apps' %self._base
    self.path_data = '%s/data' %self._base

    # Update the environment
    self.add_env('SCIF_DATA', self.path_data)
    self.add_env('SCIF_APPS', self.path_apps)

    # Check if it's writable
    if writable is True:
        if not os.access(base, os.W_OK):
            bot.error('%s is not writable.' %base)
            sys.exit(1)



def set_defaults(self, entry_point=None):
    '''set the defaults for the SCIF state at start up. 
       Usually this means parsing them from the environment. We hold these
       with the object so we can easily maintain and change state.
    '''

    # The entrypoint is the runscript (or /bin/bash default)
    self._entry_point = parse_entrypoint(entry_point)   
                                          
    # Set the default entry folder, changed to app if in context of app
    from scif.defaults import SCIF_ENTRYFOLDER
    self._entry_folder = SCIF_ENTRYFOLDER       # Defaults to None

    # The active app, coinciding with the entry_point
    self._active = None


def install_base(self):
    ''' create basic scif structure at the base for apps and metadata

        Parameters
        ==========
        base: the full path to the root folder to create /scif
    '''
    if not hasattr(self,'_base'):
        bot.error('Please set the base before installing to it.')
        sys.exit(1)

    bot.info('Installing base at %s' %self._base)  

    mkdir_p(self.path_apps)
    mkdir_p(self.path_data)
