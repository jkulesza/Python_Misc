
# IMPORT PACKAGES ##############################################################

from __future__ import print_function

import subprocess
import sys
import re

# DEFINE CONSTANTS #############################################################

MAXGRPS = 47

matdict = {}
matdict[5] = "mat_1_fuel"
matdict[6] = "mat_2_moderator"
matdict[7] = "mat_3_baffle"

# DEFINE FUNCTIONS #############################################################

# Parse VTK file to get array values.
def getarray(infile,arrayname):
    cmd = r"sed -e '1,/^LOOKUP_TABLE " + arrayname + "/d' -e '/^POINT_DATA/,$d' " + infile
    cmdout = subprocess.check_output(cmd,shell=True)
    array = cmdout.split()
    while '' in array: array.remove('')  
    return array

# Parse VTK file to segregate negative source components.
def getlist(infile, scalar_str):
    cmd = r'grep "SCALARS ' + scalar_str + '" ' + infile + ' | cut -c 9-23'
    cmdout = subprocess.check_output(cmd,shell=True)
    cmdlist = cmdout.split('\n')
    while '' in cmdlist: cmdlist.remove('')  
    return cmdlist
 
# EXECUTE PROGRAM ##############################################################

try:
    infile = sys.argv[1]
except:
    print("Error: No VTK file defined in ARGV")
    exit()

outfile = infile + ".neg"
outfile = open(outfile,'w')
 
matarray = getarray(infile,"material_table"); matarray = map(int, matarray)
print("Length of material array: " + str(len(matarray)), file=outfile)

# Collect all VTK SCALAR entries corresponding to negative sources.
nextlist = getlist(infile,"next")
nssslist = getlist(infile,"nsss")
nstrlist = getlist(infile,"nstr")
qbarlist = getlist(infile,"qbar")

# Output general diagnostic information preceded by a delimiter.
print("Operating on: " + infile, file=outfile)  
print("Found: ", file=outfile)
print("  " + "{:>5}".format(str(len(nextlist))) + " negative external source entry", file=outfile)
print("  " + "{:>5}".format(str(len(nssslist))) + " negative scattering source entry", file=outfile)
print("  " + "{:>5}".format(str(len(nstrlist))) + " negative total cross section entry", file=outfile)
print("  " + "{:>5}".format(str(len(qbarlist))) + " negative total source entry", file=outfile)
print("Total: " + str(len(nextlist)+len(nssslist)+len(nstrlist)+len(qbarlist)) + " Entries", file=outfile)
 
# Print table header.
print(101*"-", file=outfile)
print("| {:^17} | {:^17} | {:^17} | {:^17} | {:^17} |".format("Group", "Neg Ext.", "Neg. Self-Scat.", "Neg. Sig-Tr.", "Neg. Q-bar"), file=outfile)
print(101*"-", file=outfile)

# Iterate through energy groups and source components to search for negatives.
for g in range(1, MAXGRPS+1):

    # Process negative external source (next).
    next_negmat = []
    for n,i in enumerate(nextlist):
        if(i.startswith("next{:_>3}".format(g))):
            nextarray = getarray(infile,i); nextarray = map(float, nextarray)
            for o,j in enumerate(nextarray):
                if(j<0.0):
                    next_negmat.append(matarray[o])
    next_negmat = sorted(set(next_negmat))
 
    # Process negative self-scatter source (nsss).
    nsss_negmat = []
    for n,i in enumerate(nssslist):
        if(i.startswith("nsss{:_>3}".format(g))):
            nsssarray = getarray(infile,i); nsssarray = map(float, nsssarray)
            for o,j in enumerate(nsssarray):
                if(j<0.0):
                    nsss_negmat.append(matarray[o])
    nsss_negmat = sorted(set(nsss_negmat))

    # Process negative total cross-section source (nstr).
    nstr_negmat = []
    for n,i in enumerate(nstrlist):
        if(i.startswith("nstr{:_>3}".format(g))):
            nstrarray = getarray(infile,i); nstrarray = map(float, nstrarray)
            for o,j in enumerate(nstrarray):
                if(j<0.0):
                    nstr_negmat.append(matarray[o])
    nstr_negmat = sorted(set(nstr_negmat))

    # Process negative total source (qbar).
    qbar_negmat = []
    for n,i in enumerate(qbarlist):
        if(i.startswith("qbar{:_>3}".format(g))):
            qbararray = getarray(infile,i); qbararray = map(float, qbararray)
            for o,j in enumerate(qbararray):
                if(j<0.0):
                    qbar_negmat.append(matarray[o])
    qbar_negmat = sorted(set(qbar_negmat))

    print("| {:^17} | {:^17} | {:^17} | {:^17} | {:^17} |".format(  g,
                                                                    " ".join(map(str, next_negmat)),
                                                                    " ".join(map(str, nsss_negmat)),
                                                                    " ".join(map(str, nstr_negmat)),
                                                                    " ".join(map(str, qbar_negmat))), file=outfile)

print(101*"-", file=outfile)

