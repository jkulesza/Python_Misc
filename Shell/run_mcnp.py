#!/usr/bin/python

import os
import re
import subprocess
import sys

# MCNP file suffices from n= runs and logical suffices
suffices = {
             'o': '.out',
             'r': '.runtpe', 
             's': '.srctpe'
           } 
 
################################################################################
def validate_argv(argv):
    # Validate command line arguments.
    if(len(sys.argv) != 3):
        print("ERROR: Incorrect number of command line arguments provided ("
            + str(len(sys.argv)) + "); those provided:")
        print(sys.argv)
        exit()
    
    # Should validate field data - later...
    
    if(not os.path.isfile(sys.argv[2])):
        print("ERROR: MCNP input file not found.")
        exit()

    # Determine appropriate values from argv.
    np = sys.argv[1]
    fn = sys.argv[2]
    pwd = os.getcwd()

    return np, fn, pwd

################################################################################
def clean_old_MCNP_files(inpfilename):
    for k,v in suffices.iteritems():
        rmfilename = inpfilename + k
        if(os.path.isfile(rmfilename)):
            os.popen('rm ' + rmfilename).read()    
    return

################################################################################
def relocate_new_MCNP_files(inpfilename):
    if(re.search(r'\.inp$', inpfilename)):
        dotinp = True
    else:
        dotinp = False

    for k,v in suffices.iteritems():
        if(dotinp):
            fromfilename = inpfilename + k
            tofilename = re.sub(r'\.inp$', r'', inpfilename) + v
        else:
            fromfilename = inpfilename + k
            tofilename = inpfilename + v

        if(os.path.isfile(fromfilename)):
            os.popen('mv ' + fromfilename + ' ' + tofilename).read()     
    return
 
################################################################################
def run_MCNP(inpfilename, cmd):
    if(re.search(r'\.inp$', inpfilename)):
        dayfilename = re.sub(r'\.inp$', r'', inpfilename)
        f = open(dayfilename + '.day', 'w')
    else:
        f = open(inpfilename + '.day', 'w')
    
    print('Running Job...')

    print(cmd)
    
    p = subprocess.Popen(cmd, 
                         shell=True,
                         stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE)
    
    for line in iter(p.stdout.readline, b''):
        print("" + line.rstrip())
    
    f.close()
    return
 
################################################################################
# Main Program #################################################################
################################################################################

np, inpfilename, pwd = validate_argv(sys.argv)

clean_old_MCNP_files(inpfilename) 

cmd = '/data/MCNP61/MCNP_CODE/bin/mcnp6 tasks ' + np + ' n=' + inpfilename

run_MCNP(inpfilename, cmd)

relocate_new_MCNP_files(inpfilename)
