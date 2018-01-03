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
from scif.main.parser import load

bot.level = 3

class ScifRecipe:
    '''Create and work with a scif recipe. Usage typically looks like:

       recipe = ScifRecipe('sregistry.scif')
       
       Parameters
       ==========
       path: the path to the scif recipe flie.

    '''
    
    def __init__(self, path=None):
        '''initialize the scientific filesystem by creating a scif folder
           at the base, and loading the recipe to fill it.

           Parameters
           ==========
           path: is the first paramter, not required to initialize an empty 
                 client session. The logic proceeds as follows:
                 1. If path is not defined, we want (empty) interactive session
                 2. We derive the base from the environment SCIF_BASE
        '''
        # 0. base determined from environment
        from scif.defaults import SCIF_BASE as base

        # 1. Determine if path is a recipe or base
        if path is not None:

            # 1. path is a recipe
            if os.path.isfile(path):
                self.load(path)      # recipe, environment
                self.set_base(base) # /scif

            # 1. path is a base
            elif os.path.isdir(path):   
                #TODO: write functoin to try loading base from here...
                self.set_base(path) # /scif

            else:
                bot.warning('%s is not detected as a recipe or base.')
                self.set_base(base) # /scif

        # 2. Neither, development client
        else:
            bot.info('[skeleton] session!'
            bot.info('           load a recipe: client.load("recipe.scif")')
            bot.info('           change default base:  client.set_base("/")')


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
        from scif.main.environment import env
        updates = env(self._config, self._base)
        self.environment.update(updates)
