# -*- coding: utf-8 -*-


import unittest


#
# >= python-2 compatibility
#
if not hasattr(unittest.TestCase, 'assertRaisesRegex'):
    setattr(
        unittest.TestCase,
        'assertRaisesRegex',
        unittest.TestCase.assertRaisesRegexp,
    )
