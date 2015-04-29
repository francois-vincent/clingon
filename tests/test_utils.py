# -*- coding: utf-8 -*-

try:
    # for py26
    import unittest2 as unittest
except ImportError:
    import unittest

from . import captured_output

from clingon.utils import AreYouSure


class TestAreYouSure(unittest.TestCase):
    def test_default_single(self):
        ays = AreYouSure()
        with captured_output() as (out, err):
            self.assertTrue(ays(input='yes'))
            self.assertEqual(out.getvalue(), 'Are you sure [yes,y,no(default),ALL,NONE] ? ')
            self.assertEqual(err.getvalue(), '')
            self.assertTrue(ays(input='y'))
            self.assertTrue(ays(input='Y'))
            self.assertFalse(ays(input=''))
            self.assertFalse(ays(input='no'))
            self.assertFalse(ays(input='whatever'))

    def test_default_all(self):
        ays = AreYouSure()
        with captured_output() as (out, err):
            self.assertTrue(ays(input='ALL'))
        with captured_output() as (out, err):
            self.assertTrue(ays())
        self.assertEqual(out.getvalue(), '')
        ays.reset_all()
        with captured_output() as (out, err):
            self.assertFalse(ays(input=''))
        self.assertEqual(out.getvalue(), 'Are you sure [yes,y,no(default),ALL,NONE] ? ')

    def test_default_none(self):
        ays = AreYouSure()
        with captured_output() as (out, err):
            self.assertFalse(ays(input='NONE'))
        with captured_output() as (out, err):
            self.assertFalse(ays())
        self.assertEqual(out.getvalue(), '')
        ays.reset_all()
        with captured_output() as (out, err):
            self.assertTrue(ays(input='y'))
        self.assertEqual(out.getvalue(), 'Are you sure [yes,y,no(default),ALL,NONE] ? ')

    def test_default_yes(self):
        ays = AreYouSure(yes_default='y')
        with captured_output() as (out, err):
            self.assertTrue(ays(input=''))
            self.assertEqual(out.getvalue(), 'Are you sure [yes,y(default),ALL,NONE] ? ')

    def test_stderr(self):
        ays = AreYouSure(output='stderr')
        with captured_output() as (out, err):
            self.assertTrue(ays(input='yes'))
        self.assertEqual(err.getvalue(), 'Are you sure [yes,y,no(default),ALL,NONE] ? ')

    def test_message(self):
        ays = AreYouSure(message='R U OK')
        with captured_output() as (out, err):
            self.assertTrue(ays(input='y'))
        self.assertEqual(out.getvalue(), 'R U OK [yes,y,no(default),ALL,NONE] ? ')
        with captured_output() as (out, err):
            self.assertTrue(ays(message='Proceed', input='y'))
        self.assertEqual(out.getvalue(), 'Proceed [yes,y,no(default),ALL,NONE] ? ')

    def test_french(self):
        ays = AreYouSure(message="Etes-vous sûr", yes=('oui', 'o'),
                         yes_default='non', default='défault',
                         all_yes=('TOUS',), all_no=('AUCUN',))
        with captured_output() as (out, err):
            self.assertTrue(ays(input='oui'))
            self.assertEqual(out.getvalue(), 'Etes-vous sûr [oui,o,non(défault),TOUS,AUCUN] ? ')
            self.assertTrue(ays(input='o'))
            self.assertTrue(ays(input='O'))
            self.assertFalse(ays(input=''))
            self.assertFalse(ays(input='non'))
            self.assertFalse(ays(input='whatever'))


if __name__ == '__main__':
    unittest.main()
