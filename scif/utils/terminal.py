"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from __future__ import print_function

from scif.logger import bot
from subprocess import Popen, PIPE, STDOUT
import os
import shlex


################################################################################
# Software Versions
################################################################################


def get_installdir():
    """get_installdir returns the installation directory of the application
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def run_command(cmd, sudo=False, quiet=False):
    """run_command uses subprocess to send a command to the terminal.

       Parameters
       ==========
       cmd: the command to send, should be a list for subprocess
       sudo: if True (default False) command will be run asking for sudo
       quiet: skip printing output to the terminal
    """
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)

    if sudo is True:
        cmd = ["sudo"] + cmd

    process = Popen(cmd, stderr=STDOUT, stdout=PIPE)

    # Iterate through the output
    result = ""
    while True:
        output = process.stdout.readline()

        # Encode output to utf-8, if appropriate
        try:
            output = output.decode("utf-8")
        except:
            pass

        if output == "" and process.poll() is not None:
            break
        if output:
            result = "%s%s" % (result, output)
            if not quiet:
                print(output, end="")

    # Get the return code, assemble result
    output = {"message": result, "return_code": process.poll()}

    return output
