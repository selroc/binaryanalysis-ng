import sys, os
_scriptdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_scriptdir, '..','..','test'))
# import unittest
from TestUtil import *

from Parser import GifParser
from ParserException import ParserException

class TestGifParser(TestBase):
    def test_load_standard_gif_file(self):
        rel_testfile = pathlib.Path('unpackers') / 'gif' / 'test.gif'
        filename = pathlib.Path(self.testdata_dir) / rel_testfile
        self._copy_file_from_testdata(rel_testfile)
        fileresult = create_fileresult_for_path(self.unpackdir, rel_testfile)
        filesize = fileresult.filesize
        p = GifParser()
        # dummy data unpack dir
        data_unpack_dir = (self.unpackdir / rel_testfile).parent
        r = p.parse_and_unpack(fileresult, self.scan_environment, 0,
                data_unpack_dir)
        self.assertTrue(r['status'])
        self.assertEqual(r['length'], filesize)
        self.assertEqual(r['filesandlabels'], [])
        self.assertEqual(r['metadata']['width'], 3024)

    def test_gif_file_is_extracted(self):
        rel_testfile = pathlib.Path('unpackers') / 'gif' / 'test-prepend-random-data.gif'
        filename = pathlib.Path(self.testdata_dir) / rel_testfile
        self._copy_file_from_testdata(rel_testfile)
        fileresult = create_fileresult_for_path(self.unpackdir, rel_testfile)
        filesize = fileresult.filesize
        p = GifParser()
        # dummy data unpack dir
        data_unpack_dir = (self.unpackdir / rel_testfile).parent
        r = p.parse_and_unpack(fileresult, self.scan_environment, 128,
                data_unpack_dir)
        self.assertTrue(r['status'])
        self.assertEqual(r['length'], 7073713)
        unpacked_file = r['filesandlabels'][0][0]
        unpacked_labels = r['filesandlabels'][0][1]
        self.assertTrue((self.unpackdir / unpacked_file).exists())
        self.assertEqual((self.unpackdir / unpacked_file).stat().st_size, r['length'])
        self.assertEqual(r['metadata']['width'], 3024)
        self.assertSetEqual(set(unpacked_labels),
                set(r['labels'] + ['unpacked']))

    def test_load_png_file(self):
        rel_testfile = pathlib.Path('unpackers') / 'png' / 'test.png'
        filename = pathlib.Path(self.testdata_dir) / rel_testfile
        self._copy_file_from_testdata(rel_testfile)
        fileresult = create_fileresult_for_path(self.unpackdir, rel_testfile)
        # with self.assertRaises(ParserException) as context:
        #    p = GifParser()
        #    p.parse_and_unpack(fileresult, self.scan_environment, 0, self.unpackdir)
        p = GifParser()
        r = p.parse_and_unpack(fileresult, self.scan_environment, 0, self.unpackdir)
        self.assertFalse(r['status'])
        self.assertIsNotNone(r['error']['reason'])

if __name__ == '__main__':
    unittest.main()

