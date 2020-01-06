"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.main.apps import app, apps, activate, deactivate, help, inspect, reset
from scif.main.base import ScifRecipe
from scif.main.commands import _exec, execute, run, shell, test
from scif.main.environment import (
    add_env,
    append_path,
    export_env,
    get_env,
    get_append_path,
    get_appenv,
    get_appenv_lookup,
    init_env,
    load_env,
    update_env,
)
from scif.main.helpers import run_command, set_entrypoint
from scif.main.preview import (
    preview,
    preview_apps,
    preview_base,
    init_app_preview,
    preview_runscript,
    preview_labels,
    preview_environment,
    preview_files,
    preview_commands,
    preview_recipe,
    preview_test,
)
from scif.main.setup import install_base, set_base, set_defaults
from scif.main.install import (
    init_app,
    install,
    install_apps,
    install_runscript,
    install_environment,
    install_help,
    install_script,
    install_labels,
    install_commands,
    install_files,
    install_recipe,
    install_test,
)


# We can eventually add logic here for customizing the client


# Commands
ScifRecipe.execute = execute
ScifRecipe._exec = _exec
ScifRecipe.run = run
ScifRecipe.test = test
ScifRecipe.shell = shell

# Helpers
ScifRecipe._run_command = run_command
ScifRecipe._set_entrypoint = set_entrypoint
ScifRecipe.help = help

# Environment
ScifRecipe.append_path = append_path
ScifRecipe._append_path = get_append_path
ScifRecipe._init_env = init_env
ScifRecipe.add_env = add_env
ScifRecipe.export_env = export_env
ScifRecipe.get_env = get_env
ScifRecipe.load_env = load_env
ScifRecipe.update_env = update_env


# Preview
ScifRecipe.preview = preview
ScifRecipe._preview_base = preview_base
ScifRecipe._preview_apps = preview_apps
ScifRecipe._init_app_preview = init_app_preview
ScifRecipe._preview_runscript = preview_runscript
ScifRecipe._preview_labels = preview_labels
ScifRecipe._preview_environment = preview_environment
ScifRecipe._preview_commands = preview_commands
ScifRecipe._preview_files = preview_files
ScifRecipe._preview_recipe = preview_recipe
ScifRecipe._preview_test = preview_test

# Setup
ScifRecipe._install_base = install_base
ScifRecipe.set_base = set_base
ScifRecipe.set_defaults = set_defaults

# Apps
ScifRecipe.get_appenv_lookup = get_appenv_lookup
ScifRecipe.get_appenv = get_appenv
ScifRecipe.app = app
ScifRecipe.apps = apps
ScifRecipe.activate = activate
ScifRecipe.deactivate = deactivate
ScifRecipe.inspect = inspect
ScifRecipe.reset = reset

# Installation
ScifRecipe.install = install
ScifRecipe._init_app = init_app
ScifRecipe._install_apps = install_apps
ScifRecipe._install_commands = install_commands
ScifRecipe._install_environment = install_environment
ScifRecipe._install_files = install_files
ScifRecipe._install_help = install_help
ScifRecipe._install_labels = install_labels
ScifRecipe._install_recipe = install_recipe
ScifRecipe._install_runscript = install_runscript
ScifRecipe._install_script = install_script
ScifRecipe._install_test = install_test
