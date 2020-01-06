"""

Copyright (C) 2018-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.utils import run_command as run_cmd
from scif.defaults import SCIF_SHELL
from scif.logger import bot
import shlex
import os
import re


def get_parts(pair, default=None):
    """pair is expected to be a string with some key, value, and this function
       will replace any "=" with a space, and then parse the remainder
       for a first and second part (key and value pair). 

       We likely will need to use regular expressions for pairs that have 
       spaces or equals that need to be maintained.

       Parameters
       ==========
       pair should be a single string, likely with a key and value split by 
            a space or equals sign.

    """
    pair = pair.replace("=", " ")
    parts = pair.split(" ")
    src = parts[0].strip()
    if len(parts) == 1:
        dest = default
    else:
        dest = parts[1].strip()
    return src, dest


def run_command(self, cmd, spinner=True, quiet=True):
    """run_command will run a command (a list) and wrap in a spinner. A 
       result (dict) with message and return code is returned. If the
       return value is not 0, an error is issed and we exit
    """
    if spinner is True:
        bot.spinner.start()

    result = run_cmd(cmd, quiet=quiet)

    if spinner is True:
        bot.spinner.stop()

    retval = result["return_code"]

    # Beep boop, error!
    if retval != 0:
        bot.exit("Return code %s" % retval, retval)

    return result


def set_entrypoint(self, app, config_key="SCIF_APPRUN", args=None):
    """if the value is defined in the config and the file exists, set
       the entrypoint for the app to execute the script.

       Parameters
       ==========
       key: the entry in the config (a filename) to check for existence. If 
            it exists, then set it's execution using the default shell to
            be the entrypoint.

       returns True if the config entry and file are found, False otherwise
    """

    if app in self.apps():
        config = self.get_appenv(app)

        if config_key in config:
            if os.path.exists(config[config_key]):
                self._entry_point = [SCIF_SHELL, config[config_key]]
                if args is not None:
                    args = parse_entrypoint(args)
                    self._entry_point += args
                return True
    return False


def parse_entrypoint(entry_point=None):
    """parse entrypoint will return a list, where the first argument is the
       executable, followed by arguments. This function also works to
       parse arguments into a list.
 
       Parameters
       ==========
       entry_point: the entry point for the application, is 
    """

    if entry_point is None:
        from scif.defaults import SCIF_ENTRYPOINT as entry_point

    # We expect an [executable, arg1, arg2]
    if not isinstance(entry_point, list):
        entry_point = [entry_point]

    # Special characters in the entrypoint should be replaced
    #        [e] in the command or entrypoint: environment vars --> $
    #        [out] in the command or entrypoint: environment vars --> >
    #        [in] in the command or entrypoint: environment vars --> <
    #        [pipe] in the command or entrypoint: environment vars --> |

    entry_point = " ".join(entry_point)
    entry_point = re.sub("\[e\]", "$", entry_point)
    entry_point = re.sub("\[out\]", ">", entry_point)
    entry_point = re.sub("\[in\]", "<", entry_point)
    entry_point = re.sub("\[pipe\]", "|", entry_point)
    entry_point = re.sub("\[append\]", "|", entry_point)

    # Split into executable, arguments
    return shlex.split(entry_point)
