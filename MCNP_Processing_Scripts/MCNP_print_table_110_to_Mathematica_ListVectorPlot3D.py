# IMPORT PACKAGES ##############################################################

import sys
import re

# DEFINE CONSTANTS #############################################################

# DEFINE FUNCTIONS #############################################################

# Import Print Table 110 Values
def import_print_table_110(infilename):
    infile_full = ""
    with open(infilename) as infile:
        for line in infile:
            infile_full += line            

    # Extract print table 110 with headers and title.
    table110 = re.search(r'(print table 110.*?)\n[*1]', infile_full, re.DOTALL).group(1)

    # Extract data from print table 110.
    table110 = re.sub(r'\n\s+\n',r'\n\n', table110, re.DOTALL)
    table110 = re.search(r'^.*?nps.*?\n+(.*?)$', table110, re.DOTALL).group(1)

#   print(table110)

    # Split the data into a multidimensional array.
    table110arr = [line.split() for line in table110.split('\n') 
                    if line.find('100') != -1 and line.find('100') != -1]

#   for i in table110arr:
#       print(i)

    return table110arr

# EXECUTE PROGRAM ##############################################################

try:
    infilename = sys.argv[1]
except:
    print("Error: No MCNP output file defined in ARGV")
    exit()

outfilename = infilename + ".mathematica_input"
outfile = open(outfilename,'w')

table110arr = import_print_table_110(infilename)
mathematica_input = ""
for i,n in enumerate(table110arr):
    nps = n[0]
    x   = n[1]
    y   = n[2]
    z   = n[3]
    u   = n[6]
    v   = n[7]
    w   = n[8]
    erg = n[9]
    
    # Debugging printout of key data.
#   print("{:>5} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(nps, x, y, z, u, v, w, erg))

    mathematica_input += "Arrow[{{{{{0}, {1}, {2}}}, {{{0}+{3}, {1}+{4}, {2}+{5}}}}}], \n".format(x, y, z, u, v, w)

mathematica_input += 'Cylinder[{{0, 0, -0.5}, {0, 0, 0.5}}, 0.47]}, Axes->True, AxesLabel->{"x", "y", "z"}, ViewPoint->{0,0,Infinity}]'

mathematica_input = re.sub(r"^", r"Graphics3D[{", mathematica_input)
mathematica_input = re.sub(r"(\d\.\d+)E([+-]\d+)", r"\1*10^(\2)", mathematica_input)

outfile.write(mathematica_input)

outfile.close
