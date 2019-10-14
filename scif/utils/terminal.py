'''

Copyright (C) 2017-2019 Vanessa Sochat.

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

from __future__ import print_function

from scif.logger import bot
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os
import shlex


################################################################################
# Software Versions
################################################################################

def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def run_command(cmd, sudo=False, quiet=False):
    '''run_command uses subprocess to send a command to the terminal.

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       sudo: if True (default False) command will be run asking for sudo
       quiet: skip printing output to the terminal
    '''
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)

    if sudo is True:
        cmd = ['sudo'] + cmd

    process = Popen(cmd, stderr=STDOUT, stdout=PIPE, encoding='utf8')

    # Iterate through the output
    result = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            result = "%s%s" %(result, output)
            if not quiet:
                print(output, end='')

    # Get the return code, assemble result
    output = {'message': result,
              'return_code': process.poll()}

    return output
