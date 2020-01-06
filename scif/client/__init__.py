#!/usr/bin/env python

"""

Copyright (C) 2016-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

import scif
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="scientific filesystem tools")

    # Global

    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--quiet",
        dest="quiet",
        help="suppress print output",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--writable",
        "-w",
        dest="writable",
        help="for relevant commands, if writable SCIF is needed",
        default=False,
        action="store_true",
    )

    description = "actions for Scientific Filesystem"
    subparsers = parser.add_subparsers(
        help="scif actions", title="actions", description=description, dest="command"
    )

    version = subparsers.add_parser("version", help="show software version")

    # Shell and Interactive Terminal (it)

    pyshell = subparsers.add_parser(
        "pyshell", help="Interactive python shell to scientific filesystem"
    )

    pyshell.add_argument(
        "recipe", nargs="*", help="recipe file or scientific filesystem base", type=str
    )

    shell = subparsers.add_parser(
        "shell", help="shell to interact with scientific filesystem"
    )

    shell.add_argument(
        "app",
        nargs="?",
        help="app shell to, defaults to SCIF base if not set.",
        type=str,
    )

    preview = subparsers.add_parser("preview", help="preview changes to a filesytem")

    # if the user provides more than one argument here, they are apps
    preview.add_argument(
        "recipe", nargs="*", help="recipe file for the filesystem", type=str
    )

    # Help
    help = subparsers.add_parser("help", help="look at help for an app, if it exists.")

    help.add_argument("app", nargs="*", help="app(s) to print help for", type=str)

    # Install

    install = subparsers.add_parser(
        "install", help="install a recipe on the filesystem"
    )

    install.add_argument(
        "recipe", nargs="*", help="recipe file for the filesystem", type=str
    )

    # Inspect

    inspect = subparsers.add_parser(
        "inspect", help="inspect an attribute for a scif installation"
    )

    inspect.add_argument(
        "attributes",
        nargs="*",
        help="""attribute to inspect (runscript|r),
                                                      (environment|e),
                                                      (labels|l), or (all|a) (default)""",
    )

    # Run

    run = subparsers.add_parser("run", help="entrypoint to run a scientific filesystem")

    run.add_argument(
        "cmd",
        nargs="*",
        help="app and optional arguments to target for the entry",
        type=str,
    )

    # Test

    test = subparsers.add_parser(
        "test", help="entrypoint to test an app in a scientific filesystem"
    )

    test.add_argument(
        "cmd",
        nargs="*",
        help="app and optional arguments to target for the entry",
        type=str,
    )

    # List and dump

    ls = subparsers.add_parser("apps", help="list apps installed")

    ls.add_argument(
        "-l",
        dest="longlist",
        help="show long listing, including paths",
        default=False,
        action="store_true",
    )

    dump = subparsers.add_parser("dump", help="dump recipe")

    # Execute

    execute = subparsers.add_parser(
        "exec", help="execute a command to a scientific filesystem"
    )

    execute.add_argument(
        "cmd",
        nargs="*",
        help="app and command to execute. Eg, exec appname echo $SCIF_APPNAME",
        type=str,
    )

    return parser


def get_subparsers(parser):
    """get_subparser will get a dictionary of subparsers, to help with printing help
    """

    actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers


def main():
    """main is the entrypoint to managing or interacting with an scif 
       organized filesystem.
    """

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        """print help, including the software version and active client 
           and exit with return code.
        """
        version = scif.__version__

        print("\nScientific Filesystem [v%s]" % (version))
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args, unknown = parser.parse_known_args()
    except:
        sys.exit(0)

    # If unknown arguments were provided, pass on to cmd to run
    if args.command in ["run", "exec"] and len(unknown) > 0:
        args.cmd += unknown

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ["SCIF_MESSAGELEVEL"] = "INFO"
        os.putenv("SCIF_MESSAGELEVEL", "INFO")

    if args.quiet is True:
        os.environ["SCIF_MESSAGELEVEL"] = "QUIET"
        os.putenv("SCIF_MESSAGELEVEL", "QUIET")

    # Show the version and exit
    if args.command == "version":
        print(scif.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "apps":
        from .list import main
    if args.command == "dump":
        from .dump import main
    if args.command == "exec":
        from .execute import main
    if args.command == "help":
        from .help import main
    if args.command == "inspect":
        from .inspect import main
    if args.command == "install":
        from .install import main
    if args.command == "preview":
        from .preview import main
    if args.command == "pyshell":
        from .pyshell import main
    if args.command == "run":
        from .run import main
    if args.command == "shell":
        from .shell import main
    if args.command == "test":
        from .test import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, parser=parser, subparser=subparsers[args.command])
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
