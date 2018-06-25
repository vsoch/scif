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
from scif.defaults import SCIF_BASE
from scif.utils import which
import locale
import sys
import os


def _exec(self, app=None, interactive=False, exit=False):
    '''exec is the underlying driver of both run and exec, taking a final
       SCIF and executing the command for the user.

       This function is called via self._exec, and the expectation is that
       self.run or self.exec has been called first to prepare the environment
       and SCIF settings.

       If a user wants to preserve an environment variable from the console
       it can be referenced with [e], for example $SCIF_DATA --> [e]SCIF_DATA

       Parameters
       ==========
       app: the name of the application to execute a command to
       interactive: if True, us os.system directly
       exit: exit with return code from command (for test)

    '''

    name = ''
    if app is not None and app in self.apps():
        name = '[%s] ' %app

    # If the entry folder still not set, we don't have an app
    if self._entry_folder is None:
        self._entry_folder = SCIF_BASE

    # Change directory to the relevant place
    os.chdir(self._entry_folder)

    # export environment
    runtime_environ = self.export_env() 

    # Execv to the entrypoint
    executable = which(self._entry_point[0])
    args = ''

    if len(self._entry_point) > 1:
        if exit is False:
            args = ' '.join(self._entry_point[1:])
        else:
            args = self._entry_point[1:]

    # Are we executing a command as a string?
    if not isinstance(args, list):
        cmd = "%s %s" %(executable, args)
        bot.info('%sexecuting %s' %(name, cmd))

    # or a list with execv?
    else:
        bot.info('%sexecuting %s %s' %(name, executable, ' '.join(args)))

    # Return output to console
    loc = locale.getdefaultlocale()[1]

    # A shell will run the command
    if interactive is True:

        # Will exit with error, if happens, otherwise exit with 0
        if exit is True:
            result = self._run_command(cmd=[executable] + args, 
                                       spinner=False, 
                                       quiet=self.quiet)
            sys.exit(result['return_code'])
        else:
            os.system(''.join(cmd))

    else:
        for line in os.popen(cmd):
            try:
                print(line.rstrip())
            except:
                print(line.rstrip().encode(loc))


def execute(self, app, cmd=None):
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


def shell(self, app, cmd=None):
    '''akin to execute, but specific for shell. In this case, we pass the
       calling process to the shell. We do the same steps as in run/exec:

    1. Check that the app is valid for the client. Don't proceed otherwise
    2. Set the client app to be active
    3. update the environment to indicate the app is active
    4. set the entry point for exec to be relative to the app

    Parameters
    ==========
    app: the name of the scif app to execute a command to

    '''
    from scif.defaults import SCIF_SHELL

    if cmd is None:
        cmd = SCIF_SHELL

    self.activate(app, cmd)
                            # checks for existence
                            # sets _active to app's name
                            # updates environment
                            # sets shell entrypoint

                            # interactive
    return self._exec(app, True)



def run(self, app=None, args=None):
    '''run an app. This means the following:

    1. Check that the app is valid for the client. Don't proceed otherwise
    2. Set the client app to be active
    3. update the environment to indicate the app is active
    4. set the entry point and entry folder relevant to the app

    Parameters
    ==========
    app: the name of the scif app to run
    args: a list of one or more additional arguments to pass to runscript

    '''
    self.activate(app, args=args)    # checks for existence
                                     # sets _active to app's name
                                     # updates environment
                                     # sets entrypoint
                                     # sets entryfolder

    return self._exec(app)


def test(self, app=None, args=None):
    '''test an app. This means the following:

    1. Check that the app is valid for the client. Don't proceed otherwise
    2. Set the client app to be active
    3. update the environment to indicate the app is active
    4. set the entry point and entry folder relevant to the app
    5. Run interactively, and return the entry code to the client

    Parameters
    ==========
    app: the name of the scif app to run. If none provided, all apps are tested.
    args: a list of one or more additional arguments to pass to runscript

    '''

    # Does the application have a test script?

    if app in self.apps():

        self.activate(app, args=args)

        if not self._set_entrypoint(app, 'SCIF_APPTEST', args):
            bot.info("No tests defined for this app.")
            sys.exit(1)

        return self._exec(app, interactive=True, exit=True)
