"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

import errno
import os
import re
import shutil
import stat
import codecs
import json
from scif.logger import bot


################################################################################
## FOLDER OPERATIONS ###########################################################
################################################################################


def mkdir_p(path):
    """mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.exit("Error creating path %s, exiting." % path)


def which(software):
    """which is a substitute for shutil.which, which is only supported in
       python 3
    
       Parameters
       ==========
       software: the name of the executable to find

    """
    path = os.getenv("PATH")
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, software)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


################################################################################
## FILE OPERATIONS #############################################################
################################################################################


def make_executable(filename):
    """make a file executable by doing the equivalent of chmod+x

       Parameters
       ==========
       filename: the name of the file to make executable
    """
    if os.path.exists(filename):
        st = os.stat(filename)
        mode = st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(filename, mode)


def copyfile(source, destination, force=True):
    """copy a file from a source to its destination.
    """
    if os.path.exists(destination) and force is True:
        os.remove(destination)
    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    """write_file will open a file, "filename" and write content, "content"
        and properly close the file
    """
    with codecs.open(filename, mode, encoding="utf-8") as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    """write_json will (optionally,pretty print) a json object to file

       Parameters
       ==========
       json_obj: the dict to print to json
       filename: the output file to write to
       pretty_print: if True, will use nicer formatting
    """
    with codecs.open(filename, mode, encoding="utf-8") as filey:
        if print_pretty:
            filey.writelines(json.dumps(json_obj, indent=4, separators=(",", ": ")))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_file(filename, mode="r", readlines=True):
    """write_file will open a file, "filename" and write content, "content"
       and properly close the file
    """
    with codecs.open(filename, mode, encoding="utf-8") as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode="r"):
    """read_json reads in a json file and returns
       the data structure as dict.
    """
    with codecs.open(filename, mode, encoding="utf-8") as filey:
        data = json.load(filey)
    return data
