#!/usr/bin/python

import os
import re
import subprocess
import sys

test_exec = 'Event_Log_Visualizer.py'

# Any special test case options to execute with
test_opts = {'test_01': 'outp',
             'test_02': 'outp',
             'test_03': 'outp',
             'test_04': 'outp',
             'test_05': 'outp'}

################################################################################
# Wrapper to run shell commands and report output interactively.
def runcmd(cmd, save_stdout = False, stdout_prefix = 'runcmd'):
    p = subprocess.Popen(cmd,
                         shell=True,
                         stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE)
    output = ''
    for line in iter(p.stdout.readline, b''):
        print("" + line.rstrip())
        if(save_stdout):
            output = output + line

    if(save_stdout):
        outfile = open(stdout_prefix + '.stdout', 'w')
        outfile.write(output)
        outfile.close()

    return

################################################################################
# Get list of subdirectories and remove leading 'test_' to establish default
# tests (i.e., all).
def get_test_cases():
    test_cases = next(os.walk('.'))[1]
    test_cases = [re.sub(r'^test_', '', t) for t in test_cases]
    test_cases.sort()
    return test_cases

################################################################################
# Prepend 'test_' so the user doesn't need to.
def make_test_cases(tests):
    test_cases = ['test_' + t for t in tests]
    return test_cases

################################################################################
# Clean all test subdirectories.
def clean_test_case_dirs():
    rm_list = ['*.vtp', '*.stdout', test_exec]
    for r in rm_list:
        runcmd('rm -rf test_*/' + r)
    return

################################################################################
# Clean all test subdirectories.
def run_tests(test_cases):
    for t in test_cases:
        print('+' + 79*'-')
        print('| Executing Test Case: ' + t + '.')
        print('+' + 79*'-')
        assert os.path.isdir(t)
        os.chdir(t)
        # Ensure that executable is linked in.
        runcmd('ln -sf ../../' + test_exec)
        runcmd('./' + test_exec + ' ' + test_opts[t], 
               save_stdout = True, 
               stdout_prefix = t)
        os.chdir('..')
    return

################################################################################
# Main Program #################################################################
################################################################################

if __name__ == '__main__':
    import argparse
    from argparse import RawTextHelpFormatter
    import textwrap

    # Open descriptive files.
    with open ('README.md', 'r') as myfile:
        readme = myfile.read()

    with open ('TEST_CASE_DESCRIPTIONS.md', 'r') as myfile:
        test_case_descriptions = myfile.read()

    # Find all test cases to establish default set.
    all_test_cases = get_test_cases()
    test_cases = all_test_cases

    parser = argparse.ArgumentParser(description = readme,
                                     epilog = test_case_descriptions,
                                     formatter_class = RawTextHelpFormatter)

    # List all test case numbers and exit.
    parser.add_argument('--ls',
                        action = 'store_true',
                        default = False,
                        help = 'list test case numbers and descriptions (default: false).')

    parser.add_argument('--tests', '-t',
                        type = str,
                        nargs = '+',
                        default = None,
                        help = 'space-separated list of tests to run (default: ' + ', '.join(test_cases) + ').')

    parser.add_argument('--clean',
                        action = 'store_true',
                        default = False,
                        help = 'clean test case directories of old output (default: false).')

    args = parser.parse_args()

    if(args.ls):
        print(test_case_descriptions)
        quit()

    if(args.clean):
        clean_test_case_dirs()
        quit()

    if(args.tests):
        test_cases = make_test_cases(args.tests)
    else:
        test_cases = make_test_cases(test_cases)

    run_tests(test_cases)
