#!/usr/bin/python

"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

Modified from https://github.com/Visual-mov/Colorful-Julia (MIT License)

"""

from scif.utils import get_installdir
import unittest
import tempfile
import shutil
import json
import os

print("############################################################ test_utils")


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.pwd = get_installdir()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_write_read_files(self):
        """test_write_read_files will test the functions write_file and read_file
        """
        print("Testing utils.write_file...")
        from scif.utils import write_file

        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_file(tmpfile, "hello!")
        self.assertTrue(os.path.exists(tmpfile))

        print("Testing utils.read_file...")
        from scif.utils import read_file

        content = read_file(tmpfile)[0]
        self.assertEqual("hello!", content)

        from scif.utils import write_json

        print("Testing utils.write_json...")
        print("...Case 1: Providing bad json")
        bad_json = {"Wakkawakkawakka'}": [{True}, "2", 3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        with self.assertRaises(TypeError) as cm:
            write_json(bad_json, tmpfile)

        print("...Case 2: Providing good json")
        good_json = {"Wakkawakkawakka": [True, "2", 3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_json(good_json, tmpfile)
        with open(tmpfile, "r") as filey:
            content = json.loads(filey.read())
        self.assertTrue(isinstance(content, dict))
        self.assertTrue("Wakkawakkawakka" in content)

    def test_run_command(self):
        """test running a command
        """
        print("Testing utils.run_command")
        from scif.utils import run_command

        result = run_command("echo hello world")
        self.assertTrue("hello world" in result["message"])
        self.assertEqual(0, result["return_code"])

    def test_get_installdir(self):
        """get install directory should return the base of where singularity
        is installed
        """
        print("Testing utils.get_installdir")
        from scif.utils import get_installdir

        whereami = get_installdir()
        print(whereami)
        self.assertTrue("scif" in whereami)


if __name__ == "__main__":
    unittest.main()
