from setuptools import setup, find_packages
import codecs
import os

################################################################################
# HELPER FUNCTIONS #############################################################
################################################################################


def get_lookup():
    """get version by way of scif.version, returns a
    lookup dictionary with several global variables without
    needing to import singularity
    """
    lookup = dict()
    version_file = os.path.join("scif", "version.py")
    with open(version_file) as filey:
        exec(filey.read(), lookup)
    return lookup


# Read in requirements
def get_requirements(lookup=None, key="INSTALL_REQUIRES"):
    """get_requirements reads in requirements and versions from
    the lookup obtained with get_lookup"""

    if lookup == None:
        lookup = get_lookup()

    install_requires = []
    for module in lookup[key]:
        module_name = module[0]
        module_meta = module[1]
        if "exact_version" in module_meta:
            dependency = "%s==%s" % (module_name, module_meta["exact_version"])
        elif "min_version" in module_meta:
            if module_meta["min_version"] == None:
                dependency = module_name
            else:
                dependency = "%s>=%s" % (module_name, module_meta["min_version"])
        install_requires.append(dependency)
    return install_requires


# Make sure everything is relative to setup.py
install_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(install_path)

# Get version information from the lookup
lookup = get_lookup()
VERSION = lookup["__version__"]
NAME = lookup["NAME"]
AUTHOR = lookup["AUTHOR"]
AUTHOR_EMAIL = lookup["AUTHOR_EMAIL"]
PACKAGE_URL = lookup["PACKAGE_URL"]
KEYWORDS = lookup["KEYWORDS"]
DESCRIPTION = lookup["DESCRIPTION"]
LICENSE = lookup["LICENSE"]
with open("README.md") as filey:
    LONG_DESCRIPTION = filey.read()

################################################################################
# MAIN #########################################################################
################################################################################


if __name__ == "__main__":
    INSTALL_REQUIRES = get_requirements(lookup)
    INSTALL_REQUIRES_ALL = get_requirements(lookup, "INSTALL_REQUIRES_ALL")

    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        url=PACKAGE_URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        install_requires=INSTALL_REQUIRES,
        test_suite="nose.collector",
        tests_require=["nose"],
        extras_require={"all": [INSTALL_REQUIRES_ALL]},
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Programming Language :: C",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
        ],
        entry_points={"console_scripts": ["scif=scif.client:main"]},
    )
