'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017 Vanessa Sochat.

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
from scif.defaults import SCIF_BASE
from shutil import which
import sys
import os


def exec(self, app=None):
    '''exec is the underlying driver of both run and exec, taking a final
       SCIF and executing the command for the user.

       This function is called via self._exec, and the expectation is that
       self.run or self.exec has been called first to prepare the environment
       and SCIF settings.

    '''

    name = ''
    if app is not None:
        name = '[%s] ' %app

    # If the entry folder still not set, we don't have an app
    if self._entry_folder is None:
        self._entry_folder = SCIF_BASE

    # Change directory to the relevant place
    os.chdir(self._entry_folder)

    # Get export environment (do I need to do this?)
    runtime_environ = self.export_env() 

    # Change shell to show scif active
    runtime_environ['PS1'] = "scif> "

    # Execv to the entrypoint
    executable = which(self._entry_point[0])

    args = self._entry_point

    bot.info('%sexecuting %s' %(name, executable))
    os.execve(executable, args , runtime_environ)


def execute(self, cmd, app=None):
    '''execute a command in the context of an app. This means the following:

    1. Check that the app is valid for the client. Don't proceed otherwise
    2. Set the client app to be active
    3. update the environment to indicate the app is active
    4. set the entry point for exec to be relative to the app

    Parameters
    ==========
    app: the name of the scif app to execute a command to

    '''
    self.activate(app, cmd) 
                          # checks for existence
                          # sets _active to app's name
                          # updates environment
                          # sets entrypoint
                          # sets entryfolder

    return self._exec(app)



def run(self, app=None):
    '''run an app. This means the following:

    1. Check that the app is valid for the client. Don't proceed otherwise
    2. Set the client app to be active
    3. update the environment to indicate the app is active
    4. set the entry point and entry folder relevant to the app

    Parameters
    ==========
    app: the name of the scif app to run

    '''
    self.activate(app)    # checks for existence
                          # sets _active to app's name
                          # updates environment
                          # sets entrypoint
                          # sets entryfolder

    return self._exec(app)


