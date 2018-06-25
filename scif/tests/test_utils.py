#!/usr/bin/python

# Copyright (C) 2017-2018 Vanessa Sochat.
# Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
# University.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
        '''test_write_read_files will test the functions write_file and read_file
        '''
        print("Testing utils.write_file...")
        from scif.utils import write_file
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_file(tmpfile,"hello!")
        self.assertTrue(os.path.exists(tmpfile))        

        print("Testing utils.read_file...")
        from scif.utils import read_file
        content = read_file(tmpfile)[0]
        self.assertEqual("hello!",content)

        from scif.utils import write_json
        print("Testing utils.write_json...")
        print("...Case 1: Providing bad json")
        bad_json = {"Wakkawakkawakka'}":[{True},"2",3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)        
        with self.assertRaises(TypeError) as cm:
            write_json(bad_json,tmpfile)

        print("...Case 2: Providing good json")        
        good_json = {"Wakkawakkawakka":[True,"2",3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_json(good_json,tmpfile)
        with open(tmpfile,'r') as filey:
            content = json.loads(filey.read())
        self.assertTrue(isinstance(content,dict))
        self.assertTrue("Wakkawakkawakka" in content)

    def test_run_command(self):
        '''test running a command
        '''
        print("Testing utils.run_command")
        from scif.utils import run_command
        result = run_command('echo hello world')
        self.assertTrue('hello world' in result['message'].decode('utf-8'))
        self.assertEqual(0, result['return_code'])


    def test_get_installdir(self):
        '''get install directory should return the base of where singularity
        is installed
        '''
        print("Testing utils.get_installdir")
        from scif.utils import get_installdir
        whereami = get_installdir()
        print(whereami)
        self.assertTrue('scif' in whereami)


if __name__ == '__main__':
    unittest.main()
