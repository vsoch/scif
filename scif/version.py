"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

__version__ = "0.0.81"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "scif"
PACKAGE_URL = "http://www.github.com/vsoch/scif"
KEYWORDS = "the scientific filesystem"
DESCRIPTION = "a filesystem organization for scientific software and metadata"
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ("six", {"min_version": "1.7.0"}),
    ("pygments", {"min_version": "2.1.3"}),
)

# Submodule Requirements

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES
