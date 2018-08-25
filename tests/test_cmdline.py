# -*- coding: utf-8 -*-


import os
import tempfile
import unittest


from wg_srle import __main__


class TestCase(unittest.TestCase):
    def test_sanity(self):
        with self.assertRaises(SystemExit) as cm:
            __main__.main(('dummy', '--version'))
        self.assertEqual(0, cm.exception.code)

    def test_invalid_command(self):
        with self.assertRaises(SystemExit) as cm:
            __main__.main(('dummy', 'xxx'))
        self.assertNotEqual(0, cm.exception.code)

    def test_invalid_spearator(self):

        for separator in (' ', '3', 'aa', '', '\n'):
            with self.assertRaises(SystemExit) as cm:
                __main__.main((
                    'dummy',
                    'encode',
                    '--separator', separator,
                    os.devnull,
                    os.devnull,
                ))
            self.assertNotEqual(0, cm.exception.code)

    def test_valid_encode_spearator(self):

        DECODED = b'abbcccddddeeeee'

        for separator in ('a', '|'):
            with tempfile.NamedTemporaryFile() as fout:
                with tempfile.NamedTemporaryFile() as fin:

                    fin.write(DECODED)
                    fin.flush()

                    __main__.main((
                        'dummy',
                        'encode',
                        '--separator', separator,
                        fin.name,
                        fout.name,
                    ))

                    fout.seek(0)
                    self.assertEqual(separator.encode('ascii'), fout.read(1))

    def test_valid_decode_spearator(self):

        DECODED = b'aabb'
        ENCODED = b'aa2ab2'

        with tempfile.NamedTemporaryFile() as fout:
            with tempfile.NamedTemporaryFile() as fin:

                fin.write(ENCODED)
                fin.flush()

                __main__.main((
                    'dummy',
                    'decode',
                    fin.name,
                    fout.name,
                ))

                fout.seek(0)
                self.assertEqual(DECODED, fout.read())

    def test_invalid_decode_spearator(self):

        ENCODED = b'aa2ab2'

        with tempfile.NamedTemporaryFile() as fin:

            fin.write(ENCODED)
            fin.flush()

            with self.assertRaisesRegex(RuntimeError, r'separator'):
                __main__.main((
                    'dummy',
                    'decode',
                    '--separator', '|',
                    fin.name,
                    '/dev/null',
                ))

    def test_encode_decode_ok(self):
        DECODED = b'abbcccddddeeeee'
        ENCODED = b'|a1|b2|c3|d4|e5'

        with tempfile.NamedTemporaryFile() as fout:

            with tempfile.NamedTemporaryFile() as fin:

                fin.write(DECODED)
                fin.flush()

                __main__.main((
                    'dummy',
                    'encode',
                    fin.name,
                    fout.name,
                ))

                fout.seek(0)
                self.assertEqual(ENCODED, fout.read())

            with tempfile.NamedTemporaryFile() as fout2:

                __main__.main((
                    'dummy',
                    'decode',
                    fout.name,
                    fout2.name,
                ))

                fout2.seek(0)
                self.assertEqual(DECODED, fout2.read())
