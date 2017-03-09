'''main program for unit test module
DO NOT RUN THIS FILE DIRECTLY, RUN run_test.sh instead'''

import os
import sys
import tempfile
import argparse
import shutil
import unittest
from flow.test.arguments import TESTARGS

TESTARGS['nextid'] = 1

def is_int(tcase):
    'is int test'
    try:
        int(tcase)
        return True
    except ValueError:
        return False


def iter_suite(suite, func):
    'recursive print test case'
    if isinstance(suite, unittest.BaseTestSuite):
        for subsuite in suite:
            iter_suite(subsuite, func)
    elif isinstance(suite, unittest.TestCase):
        func(suite)


def print_testcase(suite):
    'print test case id'
    print '{:>5}. {}'.format(str(TESTARGS['nextid']), suite.id())
    TESTARGS['nextid'] += 1


def list_testcases(sdir):
    'discover all test cases in test directory'
    suite = unittest.loader.defaultTestLoader.discover(sdir)
    print '\ntestcase(%s):' % sdir
    iter_suite(suite, print_testcase)
    return suite


def get_testcases(sdir):
    'return testcase list'
    tcs = [None]
    suite = unittest.loader.defaultTestLoader.discover(sdir)
    iter_suite(suite, lambda testcase: tcs.append(testcase.id()))
    return tcs

if __name__ == '__main__':
    testdir, _ = os.path.split(os.path.abspath(__file__))
    TESTARGS['testdir'] = testdir
    TESTARGS['tmpdir'] = os.path.join(testdir, '.tmp')

    parser = argparse.ArgumentParser(
        description='Fashion Ingestion System Unit Test')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all test cases')
    parser.add_argument('--no_logger', action='store_true',
                        help='do not test logger')
    parser.add_argument('--clean', action='store_true',
                        help='clean residues (logs, downloads...)')
    parser.add_argument('testcase', nargs='?')

    args = parser.parse_args()

    TESTARGS['no_logger'] = args.no_logger

    if args.clean:
        if os.path.isdir(TESTARGS['tmpdir']):
            shutil.rmtree(TESTARGS['tmpdir'])

    if args.list:
        list_testcases(testdir)
        sys.exit(0)

    if args.clean:
        if not args.testcase:
            sys.exit(0)

    if not os.path.isdir(TESTARGS['tmpdir']):
        os.mkdir(TESTARGS['tmpdir'])

    TESTARGS['tmpdir'] = tempfile.mkdtemp(dir=TESTARGS['tmpdir'])

    if args.testcase:
        if not is_int(args.testcase):
            unittest.main(module=None, argv=[sys.argv[0], args.testcase])
        else:
            idx = int(args.testcase)
            tlist = get_testcases(testdir)
            if 0 < idx < len(tlist):
                print 'run testcase: ', tlist[idx]
                unittest.main(module=None, argv=[sys.argv[0], tlist[idx]])
    else:
        unittest.main(module=None, argv=[sys.argv[0], 'discover'])
