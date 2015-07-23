#!/usr/bin/python
#
# For use with MAUI/PBS queuing systems.
#
# Execution Example: :>python queue_submit.py 16 8:00:00 inp
#

import os
import sys

# Validate command line arguments.
if(len(sys.argv) != 4):
    print("ERROR: Incorrect number of command line arguments provided ("
        + str(len(sys.argv)) + "); those provided:")
    print(sys.argv)
    exit()

# Should validate field data - later...

if(not os.path.isfile(sys.argv[3])):
    print("ERROR: MCNP input file not found.")
    exit()

# Assign arguments to well-named variables.
np = sys.argv[1]
wt = sys.argv[2]
fn = sys.argv[3]
myfn = fn + '.msub'
pwd = os.getcwd()

print(80*"-")
print("Constructing Submission Script...")
print('    np   = ' + np)
print('    wt   = ' + wt)
print('    fn   = ' + fn)
print('    myfn = ' + myfn)
print('    pwd  = ' + pwd )

f = open(myfn, 'w')

f.write('#MSUB -l procs=' + np + '\n')
f.write('#MSUB -l walltime=' + wt + '\n')
f.write('#MSUB -V' + '\n')
f.write('#MSUB -o ' + pwd + '/' + fn + '.day' + '\n')
f.write('\n')
f.write(80*'#'+'\n')
f.write('\n')
f.write('echo "Job  Started: " `date`' + '\n')
f.write('cd ' + pwd + '\n')
f.write('execution line' + fn + '\n')
f.write('sleep 2' + '\n')
f.write('mv ' + fn + 'o ' + fn + '.out' + '\n')
f.write('mv ' + fn + 'r ' + fn + '.rtp' + '\n')
f.write('mv ' + fn + 'm ' + fn + '.mctal' + '\n')
f.write('mv ' + fn + 's ' + fn + '.srctp' + '\n')
f.write('echo "Job Finished: " `date`' + '\n')
f.close()

print('Submitting Job...')
msub = os.popen('msub ' + myfn).read()

print('Submission output:')
print(msub)

print('Done Submitting.')
print(80*"-")

