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
import os
import re
import sys


# External Environment Functions

def env(config, base='/scif'):
    '''env will parse the complete SCIF namespace environment from a config.
    this will be defined for all apps to allow for easy interaction between
    them, regardless of which individual app is active.
    
    Parameters
    ==========
    config: the config loaded in with "load" in this file.

    Example: the following environment variables would be defined for an app
             called "google-drive" Note that for the variable, the slash is
             replaced with an underscore

             SCIF_APPDATA_google_drive=/scif/data/google-drive
             SCIF_APPRUN_google_drive=/scif/apps/google-drive/scif/runscript
             SCIF_APPHELP_google_drive=/scif/apps/google-drive/scif/runscript.help
             SCIF_APPROOT_google_drive=/scif/apps/google-drive
             SCIF_APPLIB_google_drive=/scif/apps/google-drive/lib
             SCIF_APPMETA_google_drive=/scif/apps/google-drive/scif
             SCIF_APPBIN_google_drive=/scif/apps/google-drive/bin
             SCIF_APPENV_google_drive=/scif/apps/google-drive/scif/environment.sh
             SCIF_APPLABELS_google_drive=/scif/apps/google-drive/scif/labels.json

        These paths and files are not created at this point, but just defined.

    '''
    envars = dict()
    if "apps" in config:
        for name, app in config['apps'].items(): 

            appenv = get_appenv(name, base)
            for varname, varval in appenv[name].items():
                updates = mk_env(name, varname, varval)
                envars.update(updates)

    return envars


def mk_env(key, val, app=None):
    '''a helper function to return a dictionary with a SCIF prefixed app name,
       the key slashes replaced with underscores, and the value set.

    Parameters
    ==========
    app: the app name to define the variable for (not used if not defined)
    key: the key (not including the SCIF_ prefix
    val: the value to set
    '''
    key = "SCIF_%s" % key.upper()
    if app is not None:
        key = "_%s" %app
    key = key.replace('-','_')
    return { key:val }


def get_appenv(app, base):
    '''get_appenv will create a dictionary with a highest level index the
       app name, and underneath a generic lookup (without the app name) for
       different variable types.  Eg, app with name "google-drive" would look
       like:


       {'registry': {
                      'appbin': '/scif/apps/registry/bin',
                      'appdata': '/scif/data/registry',
                      'appenv': '/scif/apps/registry/scif/environment.sh',
                      'apphelp': '/scif/apps/registry/scif/runscript.help',
                      'applabels': '/scif/apps/registry/scif/labels.json',
                      'applib': '/scif/apps/registry/lib',
                      'appmeta': '/scif/apps/registry/scif',
                      'apprecipe': '/scif/apps/registry/scif/registry.scif'
                      'approot': '/scif/apps/registry',
                      'apprun': '/scif/apps/registry/scif/runscript'
                    }            
       }

       This function is intended to be shared by env above and the environment
       generating functions in the main client, to have consistent behavior. 
       The above data structure gets parse into the (global) variables for
       the particular app:

       {'SCIF_APPBIN_registry': '/scif/apps/registry/bin',
        'SCIF_APPDATA_registry': '/scif/data/registry',
        'SCIF_APPENV_registry': '/scif/apps/registry/scif/environment.sh',
        'SCIF_APPHELP_registry': '/scif/apps/registry/scif/runscript.help',
        'SCIF_APPLABELS_registry': '/scif/apps/registry/scif/labels.json',
        'SCIF_APPLIB_registry': '/scif/apps/registry/lib',
        'SCIF_APPMETA_registry': '/scif/apps/registry/scif',
        'SCIF_APPRECIPE_registry': '/scif/apps/registry/scif/registry.scif',
        'SCIF_APPROOT_registry': '/scif/apps/registry',
        'SCIF_APPRUN_registry': '/scif/apps/registry/scif/runscript'}

    '''
    envars = {app:{}}

    # Roots for app data and app files
    appdata = "%s/data/%s" %(base, app)
    approot = "%s/apps/%s" %(base, app)
    appmeta = "%s/scif"  %(approot)

    envars[app]['appdata'] = appdata
    envars[app]['approot'] = approot
    envars[app]['appmeta'] = appmeta

    envars[app]['appbin'] = "%s/bin"  %(approot)
    envars[app]['applib'] = "%s/lib"  %(approot)
    envars[app]['apprun'] = "%s/runscript"  %(appmeta)
    envars[app]['apphelp'] = "%s/runscript.help"  %(appmeta)
    envars[app]['applabels'] = "%s/labels.json"  %(appmeta)
    envars[app]['appenv'] = "%s/environment.sh"  %(appmeta)
    envars[app]['apprecipe'] = "%s/%s.scif"  %(appmeta, app)
    envars[app]['appname'] = app

    return envars


# ScifRecipe Environment Helpers

def add_env(self, key, value):
    '''add a key/value pair to the environment. Should begin with SCIF
       to maintain proper namespace

    Parameters
    ==========
    key: the environment variable name. For SCIF, slashes should be 
         removed and replaced with underscore.
    value: the value to set for the environment variable

    '''    
    if not hasattr(self,'environment'):
        self.environment = dict()

    if not key.startswith('SCIF'):
        msg = 'Environment variable outside SCIF namespace not recommended.'
        bot.warning(msg)

    # If the variable already exists, status is "update"
    action = 'new'
    if key in self.environment:
        action = 'update'

    self.environment[key] = value
    bot.info('[environment:%s][%s:%s]' %(action.ljust(5), key, value))


def get_env(self, key=None):
    '''return a particular value for an environment variable, if the key
       exists. If no keys are defined, the entire environment is returned.
       For an app-specific environment, use get_appenv.
    '''
    if key is not None:
       if key in self.environment:
           bot.info(self.environment[key])
           return self.environment[key]

    # otherwise, return the entire environment lookup
    if hasattr(self, 'environment'):
        return self.environment
