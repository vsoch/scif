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
from scif.recipes.parser import load
from scif.recipes.environment import ( add_env, env, get_env, get_appenv )
from scif.recipes.apps import ( app, apps, get_appenv )
from scif.recipes.setup import ( init_base, set_base )
from scif.recipes.helpers import run_command
from scif.recipes.install import (
    init_app,
    install,
    install_app,
    install_runscript,
    install_environment,
    install_labels,
    install_commands,
    install_files,
    install_recipe
)


bot.level = 3

class ScifRecipe:
    '''Create and work with a scif recipe. Usage typically looks like:

       recipe = ScifRecipe('sregistry.scif')
       
       Parameters
       ==========
       path: the path to the scif recipe flie.

    '''
    
    def __init__(self, path, base='/'):
        '''initialize the scientific filesystem by creating a scif folder
           at the base, and loading the recipe to fill it.
        '''
        self._set_base(base) # /scif
        self.load(path)      # recipe, environment

    def __str__(self):
        return '[scif]'

    def __repr__(self):
        return '[scif]'

    def load(self, path):
        '''load a scif recipe into the object

        Parameters
        ==========
        path: the complete path to the config (recipe file) to load

        '''
        self._config = load(path)

        # Update environment with app information
        updates = env(self._config, self._base)
        self.environment.update(updates)
    

# Helpers
ScifRecipe._run_command = run_command
ScifRecipe.add_env = add_env
ScifRecipe.get_env = get_env

# Setup
ScifRecipe._install_base = init_base
ScifRecipe._set_base = set_base

# Apps
ScifRecipe.get_appenv = get_appenv
ScifRecipe.app = app
ScifRecipe.apps = apps

# Installation
ScifRecipe.install = install
ScifRecipe._init_app = init_app
ScifRecipe._install_app = install_app
ScifRecipe._install_runscript = install_runscript
ScifRecipe._install_environment = install_environment
ScifRecipe._install_labels = install_labels
ScifRecipe._install_commands = install_commands
ScifRecipe._install_files = install_files
ScifRecipe._install_recipe = install_recipe
