# IMPORT PACKAGES ##############################################################

import sys
import re

# DEFINE CONSTANTS #############################################################

# EXECUTE PROGRAM ##############################################################

try:
    infilename = sys.argv[1]
except:
    print("Error: No MCNP output file defined in ARGV")
    exit()

outfilename = infilename + ".collisions"
outfile = open(outfilename,'w')

infile_full = ""
with open(infilename) as infile:
    for line in infile:
        infile_full += line            

# Extract tally values of interest.
type1tally = re.search(r'(1tally.*?tally type 1.*?)1tally', infile_full, re.DOTALL).group(1)

# Match each group from 'surface' to the end of the tally uncertainty '#.####'. 
type1tallyarr = re.findall(r'surface.*?\d.\d{4}\n', type1tally, re.DOTALL)

for n,i in enumerate(type1tallyarr):
    tmp = re.search(r'surface.*?(\d+).*?user.*?bin.*?(\d\.\d+E[+-]\d+).*?angle\s+bin:(.*?)to(.*?) mu.*?(\d\.\d+E[+-]\d+) (\d.\d+)',i,re.DOTALL)
    if(tmp != None):
        surface = int(float(tmp.group(1)))
        userbin = int(float(tmp.group(2)))
        angbinl = float(tmp.group(3))
        angbinu = float(tmp.group(4))
        tally   = float(tmp.group(5))
        error   = float(tmp.group(6))

    tmp = re.search(r'surface.*?(\d+).*?user.*?bin.*?(total).*?angle\s+bin:(.*?)to(.*?) mu.*?(\d\.\d+E[+-]\d+) (\d.\d+)',i,re.DOTALL)
    if(tmp != None):
        surface = int(float(tmp.group(1)))
        userbin = tmp.group(2)
        angbinl = float(tmp.group(3))
        angbinu = float(tmp.group(4))
        tally   = float(tmp.group(5))
        error   = float(tmp.group(6))
 
    if(angbinl == -1.0):
        outfile.write("{0:>10}, {1:8.5e}, {2:5.4f},".format(userbin, tally, error))

    if(angbinl ==  0.0):
        outfile.write("{0:>10}, {1:8.5e}, {2:5.4f}\n".format(userbin, tally, error))
 
outfile.close()
