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
import sys
import os

def get_appenv(self, app, isolated=False):
    '''return environment for a specific app, meaning the variables active
       when it is running. If isolated is True, don't include other apps.

       Parameters
       ==========
       app: the new of the app to get the environment for
       isolated: if True don't include other apps
    '''
    if app in self.apps():
        environ = get_appenv(app, self._base)
        if isolated is False and hasattr(self,'environment'):
            environ.update(self.environment)
        return environ

    # if we get down here, didn't have the app in the first place
    valid = ' '.join(self.apps())
    bot.error('%s is not a valid app. Found %s' %(app, valid))


def app(self, app):
    '''view a single app, if it exists

    Parameters
    ==========
    app: the name of the app to view
        '''
    if 'apps' in self._config:
        if app in self._config['apps']:
            return self._config['apps'][app]

def apps(self):
    '''get a list of apps to show the user
    '''
    apps = []
    if "apps" in self._config:
        apps = list(self._config['apps'])
    return apps
