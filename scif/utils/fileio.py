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

import errno
import os
import re
import shutil
import codecs
import json
from scif.logger import bot
import sys


############################################################################
## FOLDER OPERATIONS #######################################################
############################################################################


def mkdir_p(path):
    '''mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


def which(software):
    '''which is a substitute for shutil.which, which is only supported in
       python 3
    
       Parameters
       ==========
       software: the name of the executable to find

    '''
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, software)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p


############################################################################
## FILE OPERATIONS #########################################################
############################################################################

def copyfile(source, destination, force=True):
    '''copy a file from a source to its destination.
    '''
    if os.path.exists(destination) and force is True:
        os.remove(destination)
    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with codecs.open(filename, mode, encoding='utf-8') as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting
    '''
    with codecs.open(filename, mode, encoding='utf-8') as filey:
        if print_pretty:
            filey.writelines(
                json.dumps(
                    json_obj,
                    indent=4,
                    separators=(
                        ',',
                        ': '))
                )
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def read_file(filename, mode="r", readlines=True):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with codecs.open(filename, mode, encoding='utf-8') as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode='r'):
    '''read_json reads in a json file and returns
    the data structure as dict.
    '''
    with codecs.open(filename, mode, encoding='utf-8') as filey:
        data = json.load(filey)
    return data
