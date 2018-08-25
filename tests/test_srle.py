# -*- coding: utf-8 -*-


import io
import os
import string
import unittest


from wg_srle import SRLE


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

        self.longMessage = True

    def test_sanity(self):
        VECTORS = [
            {
                'name': 'empty',
                'decoded': b'',
                'encoded': b'',
            },
            {
                'name': 'basic',
                'decoded': b'a',
                'encoded': b'|a1',
            },
            {
                'name': 'extended',
                'decoded': b'aaaabbbbbcccccc',
                'encoded': b'|a4|b5|c6',
            },
            {
                'name': 'unprintable',
                'decoded': b'aaabbb\n\n\n\nccc',
                'encoded': b'|a3|b3|\\x0a4|c3',
            },
            {
                'name': 'long',
                'decoded': (b'a' * 22) + (b'c' * 555) + (b'\xff' * 33),
                'encoded': b'|a22|c555|\\xff33',
            },
            {
                'name': 'use escape',
                'decoded': b'||||&&&&\\\\\\',
                'encoded': b'|\\x7c4|&4|\\x5c3',
            },
        ]

        srle = SRLE()
        for v in VECTORS:
            print('vector: %s' % v['name'])
            sout = io.BytesIO()
            srle.encode(io.BytesIO(v['decoded']), sout)
            self.assertEqual(
                v['encoded'],
                sout.getvalue(),
                msg='Vector %s' % v['name'],
            )
            sout2 = io.BytesIO()
            sout.seek(0)
            srle.decode(sout, sout2)
            self.assertEqual(
                v['decoded'],
                sout2.getvalue(),
                msg='Vector %s' % v['name']
            )

    def test_decode_special(self):

        VECTORS = [
            {
                'name': 'zero-size',
                'decoded': b'aabbbcccc',
                'encoded': b'|a2|x0|b3|c4',
            },
            {
                'name': 'separator-not-escaped',
                'decoded': b'aa|||cccc',
                'encoded': b'|a2||3|c4',
            },
        ]

        srle = SRLE()
        for v in VECTORS:
            print('vector: %s' % v['name'])
            sout = io.BytesIO()
            srle.decode(io.BytesIO(v['encoded']), sout)
            self.assertEqual(
                v['decoded'],
                sout.getvalue(),
                msg='Vector %s' % v['name']
            )

    def test_decode_edge(self):
        VECTORS = [
            {
                'name': 'only-separator',
                'encoded': b'|',
                'pattern': r'character',
            },
            {
                'name': 'only-separator-and-byte',
                'encoded': b'|a',
                'pattern': r'numeric',
            },
            {
                'name': 'invalid-next-separator',
                'encoded': b'|a12x',
                'pattern': r'separator',
            },
            {
                'name': 'only-next-separator',
                'encoded': b'|a12|',
                'pattern': r'character',
            },
            {
                'name': 'escape-only',
                'encoded': b'|\\',
                'pattern': r"'x'",
            },
            {
                'name': 'escape-only-x',
                'encoded': b'|\\x',
                'pattern': r'two digits',
            },
            {
                'name': 'escape-single-digit',
                'encoded': b'|\\x1',
                'pattern': r'two digits',
            },
            {
                'name': 'escape-single-digit-and-non-digit',
                'encoded': b'|\\x1x',
                'pattern': r'hex',
            },
            {
                'name': 'escape-single-digit-and-separator',
                'encoded': b'|\\x1|',
                'pattern': r'hex',
            },
            {
                'name': 'no-size-end-and-of-stream',
                'encoded': b'|\\x12',
                'pattern': r'numeric',
            },
            {
                'name': 'no-size-and-separator',
                'encoded': b'|\\x12|',
                'pattern': r'numeric',
            },
            {
                'name': 'no-size-and-non-digit',
                'encoded': b'|\\x12x',
                'pattern': r'numeric',
            },
            {
                'name': 'non-ascii-as-digit',
                'encoded': b'|x\xff',
                'pattern': r'numeric',
            },
            {
                'name': 'non-ascii-after-size',
                'encoded': b'|x12\xff',
                'pattern': r'separator',
            },
        ]

        srle = SRLE()

        for v in VECTORS:
            print('vector: %s' % v['name'])
            with self.assertRaisesRegex(RuntimeError, v['pattern']):
                srle.decode(io.BytesIO(v['encoded']), io.BytesIO())

    def test_decode_guess_separator(self):
        DECODED = b'aabbbcccc'
        ENCODED = b'xa2xb3xc4'

        srle = SRLE(separator=None)
        sout = io.BytesIO()
        srle.decode(io.BytesIO(ENCODED), sout)
        self.assertEqual(
            DECODED,
            sout.getvalue(),
        )

    def test_decode_guess_separator_fail(self):
        ENCODED = b'xa2yb3xc4'

        srle = SRLE(separator=None)
        with self.assertRaisesRegex(RuntimeError, r'separator'):
            srle.decode(io.BytesIO(ENCODED), io.BytesIO())

    def test_decode_guess_separator_invalid(self):
        ENCODED = b'\xffa2\xffb3\xffc4'

        srle = SRLE(separator=None)
        with self.assertRaisesRegex(RuntimeError, r'separator'):
            srle.decode(io.BytesIO(ENCODED), io.BytesIO())

    def test_custom_separator(self):

        SEPARATORS = ('|', 'x', SRLE.ESCAPE)
        DECODED = b'aabbbcccc'
        ENCODED = '|a2|b3|c4'

        for s in SEPARATORS:
            srle = SRLE(separator=s)

            sout = io.BytesIO()
            srle.encode(io.BytesIO(DECODED), sout)
            self.assertEqual(
                ENCODED.replace('|', srle.separator).encode('ascii'),
                sout.getvalue(),
            )
            sout.seek(0)
            sout2 = io.BytesIO()
            srle.decode(sout, sout2)
            self.assertEqual(
                DECODED,
                sout2.getvalue(),
            )

    def test_separator_as_char_no_escape(self):
        DECODED = b'aabbbcccc'
        ENCODED = b'|a2|x0|b3|c4'

        srle = SRLE()
        sout = io.BytesIO()
        srle.decode(io.BytesIO(ENCODED), sout)
        self.assertEqual(
            DECODED,
            sout.getvalue(),
        )

    def test_random(self):

        for n in range(10):

            DECODED = os.urandom(4096)

            srle = SRLE()
            sout = io.BytesIO()
            srle.encode(io.BytesIO(DECODED), sout)
            sout.seek(0)
            sout2 = io.BytesIO()
            srle.decode(sout, sout2)
            self.assertEqual(
                DECODED,
                sout2.getvalue(),
            )

    def test_invalid_decode_spearator(self):

        with self.assertRaisesRegex(ValueError, r'Separator'):
            SRLE(separator='')
        for separator in string.digits + string.whitespace + '\xff':
            with self.assertRaisesRegex(ValueError, r'Separator'):
                SRLE(separator=separator)
