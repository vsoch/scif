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


def _exec(self, app=None):
    '''exec is the underlying driver of both run and exec, taking a final
       SCIF and executing the command for the user.

       This function is called via self._exec, and the expectation is that
       self.run or self.exec has been called first to prepare the environment
       and SCIF settings.

       If a user wants to preserve an environment variable from the console
       it can be referenced with [e], for example $SCIF_DATA --> [e]SCIF_DATA
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
        args = ' '.join(self._entry_point[1:])

    cmd = "%s %s" %(executable, args)
    bot.info('%sexecuting %s' %(name, cmd))

    # Return output to console
    loc = locale.getdefaultlocale()[1]

    for line in os.popen(cmd):
        print(line)
        try:
            print(line.rstrip())
        except:
            print(line.rstrip().encode(loc))


import subprocess
import re

def run_command(cmd, sudo=False, capture=True, no_newline_regexp="Progess"):
    '''run_command uses subprocess to send a command to the terminal. If
       capture is True, we use the parent stdout, so the progress bar (and
       other commands of interest) are piped to the user. This means we 
       don't return the output to parse.

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       sudo: if needed, add to start of command
       no_newline_regexp: the regular expression to determine skipping a
                          newline. Defaults to finding Progress
       capture: if True, don't set stdout and have it go to console. This
                option can print a progress bar, but won't return the lines
                as output.
    '''

    if sudo is True:
        cmd = ['sudo'] + cmd

    stdout = None
    if capture is True:
        stdout = subprocess.PIPE

    # Use the parent stdout and stderr
    process = subprocess.Popen(cmd, 
                               stderr = subprocess.PIPE, 
                               stdout = stdout)
    lines = ()
    found_match = False

    for line in process.communicate():
        if line:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            lines = lines + (line,)
            if re.search(no_newline_regexp, line) and found_match is True:
                sys.stdout.write(line)
                found_match = True
            else:
                print(line.rstrip())
                found_match = False

    output = {'message': lines,
              'return_code': process.returncode }

    return output





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
