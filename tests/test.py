from easyprocess import Proc
from nose.tools import eq_, ok_
from unittest import TestCase
import os.path
# from path import path

d = os.path.dirname(__file__)
example1_py = os.path.join(d, 'example1.py')
example2_py = os.path.join(d, 'example2.py')
example3_py = os.path.join(d, 'example3.py')


class Test(TestCase):
    def test_1_call(self):
        import example1
        eq_(example1.f(3), 3)
        eq_('description' in example1.f.__doc__, True)
        eq_(example1.f.__name__, 'f')

    def test_2_call(self):
        import example2
        eq_(example2.f(5, 1), 6)
        eq_(example2.f.__doc__, None)
        eq_(example2.f.__name__, 'f')

    def test_3_call(self):
        import example3
        eq_(example3.f(), 7)
        eq_(example3.f.__doc__, None)
        eq_(example3.f.__name__, 'f')

    def test_1_cli(self):
        cmd = 'python %s 5' % example1_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

        cmd = 'python %s 5 --two 7 --debug' % example1_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

        cmd = 'python %s 5 --three -t 2 --debug' % example1_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

        cmd = 'python %s 5 -t x' % example1_py
        p = Proc(cmd).call()
        eq_(p.return_code > 0, 1)
        eq_(p.stdout, '')
        eq_(p.stderr != '', 1)

        cmd = 'python %s -t 1  5  --debug' % example1_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

    def test_2_cli(self):
        cmd = 'python %s 5 2' % example2_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

        cmd = 'python %s --debug    5 2' % example2_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        ok_('root - DEBUG - 5' in p.stderr)

    def test_3_cli(self):
        cmd = 'python %s ' % example3_py
        p = Proc(cmd).call()
        eq_(p.return_code, 0)
        eq_(p.stdout, '')
        eq_(p.stderr, '')

    def test_1_ver(self):
        cmd = 'python %s --version' % example1_py
        p = Proc(cmd).call()
        eq_(p.stdout, '')
        eq_(p.stderr, '3.2')
        eq_(p.return_code, 0)

    def test_2_ver(self):
        cmd = 'python %s --version' % example2_py
        p = Proc(cmd).call()
        eq_(p.stdout, '')
        eq_(p.stderr, '1.2')
        eq_(p.return_code, 0)

    def test_3_ver(self):
        cmd = 'python %s --version' % example3_py
        p = Proc(cmd).call()
        eq_(p.stdout, '')
        self.assertNotEqual(p.stderr, '')
        self.assertNotEqual(p.return_code, 0)

    def test_1_help(self):
        cmd = 'python %s --help' % example1_py
        p = Proc(cmd).call()
        eq_(p.stderr, '')
        eq_(p.return_code, 0)
        eq_('one' in p.stdout, 1)
        eq_('--two' in p.stdout, 1)
        eq_('-t' in p.stdout, 1)
        eq_('--three' in p.stdout, 1)

    def test_2_help(self):
        cmd = 'python %s --help' % example2_py
        p = Proc(cmd).call()
        eq_(p.stderr, '')
        eq_(p.return_code, 0)

    def test_3_help(self):
        cmd = 'python %s --help' % example3_py
        p = Proc(cmd).call()
        eq_(p.stderr, '')
        eq_(p.return_code, 0)
