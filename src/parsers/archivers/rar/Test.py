import sys, os
from test.TestUtil import *

from .UnpackParser import RarUnpackParser

class TestRarUnpackParser(TestBase):
    def test_load_standard_file(self):
        rel_testfile = pathlib.Path('a') / 'hachoir-core.rar'
        self._copy_file_from_testdata(rel_testfile)
        fileresult = create_fileresult_for_path(self.unpackdir, rel_testfile,
                set())
        filesize = fileresult.filesize
        p = RarUnpackParser(fileresult, self.scan_environment)
        # dummy data unpack dir
        p.open()
        data_unpack_dir = rel_testfile.parent / 'some_dir'
        r = p.parse_and_unpack(fileresult, self.scan_environment, 0,
                data_unpack_dir)
        p.close()
        self.assertTrue(r['status'])
        self.assertEqual(r['length'], filesize)
        self.assertEqual(len(r['filesandlabels']), 0)

if __name__ == '__main__':
    unittest.main()

