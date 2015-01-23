#!/bin/python

import getopt
import math
import re
import string
import sys

import NuclearData_NIST as NuclearData

# Define constants.
#N_A      = 0.59703109E24  # Avogadro's number from MCNP.
N_A      = 0.60221413e+24  # Standard Avogadro's number.
bnpercm2 = 1.0E24          # 10^24 barns per cm^2.

################################################################################
#
# Convert w/o to a/o.  
#    
################################################################################
def wo_to_ao(inp, bulk_density):
    zaid_mass = []
    for i in inp:
        zaid = i[0]
        zaid_mass.append(NuclearData.Masses[zaid])

    wo_per_mass = []
    for i in enumerate(inp):
        wo = i[1][1]
        wo_per_mass.append(wo / zaid_mass[i[0]])
 
    total_fraction = []
    for i in enumerate(inp):
        total_fraction.append(wo_per_mass[i[0]] * sum(zaid_mass))
 
    ao = []
    for i in enumerate(inp):
        ao.append(total_fraction[i[0]] / sum(total_fraction))

    out = []
    for i in enumerate(inp):
        out.append([i[1][0],ao[i[0]]])

    return(out, bulk_density)

################################################################################
#
# Convert a/o to w/o.  
#    
################################################################################
def ao_to_wo(inp, bulk_density):
    zaid_mass = []
    for i in inp:
        zaid = i[0]
        zaid_mass.append(NuclearData.Masses[zaid])

    ao_by_mass = []
    for i in enumerate(inp):
        ao = i[1][1]
        ao_by_mass.append(ao * zaid_mass[i[0]])
 
    wo = []
    for i in enumerate(inp):
        wo.append(ao_by_mass[i[0]] / sum(ao_by_mass))

    out = []
    for i in enumerate(inp):
        out.append([i[1][0],wo[i[0]]])

    return(out, bulk_density)

################################################################################
#
# Convert a/bn-cm to w/o.  
#
################################################################################
def abncm_to_wo(inp, bulk_density):
    zaid_mass = []
    for i in inp:
        zaid = i[0]
        zaid_mass.append(NuclearData.Masses[zaid])

    g_per_cc = []
    for i in enumerate(inp):
        abncm = i[1][1]
        g_per_cc.append(abncm * bnpercm2 / N_A * zaid_mass[i[0]])

    wo = []
    for i in enumerate(inp):
        wo.append(g_per_cc[i[0]] / sum(g_per_cc))

    out = []
    for i in enumerate(inp):
        out.append([i[1][0],wo[i[0]]])

    return(out, bulk_density)

################################################################################
#
# Convert w/o to a/bn-cm.  
#
################################################################################
def wo_to_abncm(inp, bulk_density):
    zaid_mass = []
    for i in inp:
        zaid = i[0]
        zaid_mass.append(NuclearData.Masses[zaid])

    density_frac = []
    for i in enumerate(inp):
        wo = i[1][1]
        density_frac.append(wo * bulk_density)

    abncm = []
    for i in enumerate(inp):
        abncm.append(density_frac[i[0]] * N_A / (zaid_mass[i[0]] * bnpercm2))

    out = []
    for i in enumerate(inp):
        out.append([i[1][0],abncm[i[0]]])
 
    return(out, bulk_density)

################################################################################
#
# Checks whether what was passed in is an integer or not.
#
################################################################################
def isInt(s):
    try: 
        int(s)
        return(True)
    except ValueError:
        return(False)

################################################################################
#
# Prints help for using command line arguments.
#    
################################################################################ 
def printHelp():
    print("""
    usage: NumberDensityConverter.py [options]
      options:
         -h, --help             Display this message.
         -c, --cli              Enters command line interface input mode.
         -f, --file=<filename>  Executes based on input file. 
         -g, --gui              Launches a GUI for interactive use.

    Report bugs to: kuleszj@westinghouse.com
            """)
    return

################################################################################
#
# Get user input.
#    
################################################################################ 
def getInput(inlabel):
    inp = []
    i = [-1]
    while(int(i[0]) != 0):
        i = raw_input("Enter ZAID, Short Name, or Long Name " + \
                      "followed by the associated " + inlabel + \
                      " value " + \
                      "(enter 0 to finish): ")
        
        i = re.split('\s+|,|;|:',i)
        if(isInt(i[0])):
            if(int(i[0]) == 0):
                next
            else:
                if(NuclearData.Masses.has_key(int(i[0]))):
                    inp.append([int(i[0]),float(i[1])])
                    printOutputTable(inp, inlabel)
                    i = [-1]
                else:
                    print("Can't find that ZAID.")  
        elif(len(i) != 2):
            print("Couldn't find ID AND " + inlabel + " value, exiting.")
            sys.exit(2)
        else:
            if(NuclearData.Full_Name.has_key(i[0].lower())):
                n = NuclearData.Full_Name[i[0].lower()]
                inp.append([n,float(i[1])])
                printOutputTable(inp, inlabel)
                i = [-1]
            elif(NuclearData.Short_Name.has_key(i[0].lower())):
                n = NuclearData.Short_Name[i[0].lower()]
                inp.append([n,float(i[1])])
                printOutputTable(inp, inlabel)
                i = [-1]
            else:
                print("Can't find that name.")
                i = [-1]

    bulk_density = raw_input("What is the material " + \
                             "bulk density (g/cc)? ")
    bulk_density = float(bulk_density) 

    return(inp, bulk_density)

################################################################################
#
# Prints output table.
#    
################################################################################ 
def printOutputTable(inp, inlabel, \
                     outlabel = None, bulk_density = None, out = None):

    if(out == None):
        print("")
        print(
              "{:>8s}   ".format("ZAID") + \
              "{:<8s}   ".format("Species") + \
              "{:>20s}   ".format("Input (" + inlabel + ")")
             ) 
    else:
        print("")
        print(
              "{:>8s}   ".format("ZAID") + \
              "{:<8s}   ".format("Species") + \
              "{:>20s}   ".format("Mass (amu)") + \
              "{:>20s}   ".format("Input (" + inlabel + ")") + \
              "{:>20s}   ".format("Bulk Density (g/cc)") + \
              "{:>20s}   ".format("Output (" + outlabel + ")")
             )  

    insum = [ sum(x) for x in zip(*inp) ][1]

    if(out == None):
        for i in enumerate(inp):
            n = NuclearData.Names[i[1][0]]
            print(
                  "{:>8d}   ".format(i[1][0]) + \
                  "{:<8s}   ".format(n) + \
                  "{:>20.9f}   ".format(i[1][1]) 
                 ) 
    else:
        for i in enumerate(inp):
            n = NuclearData.Names[i[1][0]]
            m = NuclearData.Masses[i[1][0]]
            print(
                  "{:>8d}   ".format(i[1][0]) + \
                  "{:<8s}   ".format(n) + \
                  "{:>20.9f}   ".format(m) + \
                  "{:>20.9f}   ".format(i[1][1]) + \
                  "{:>20.9f}   ".format(bulk_density) + \
                  "{:>20.9f}   ".format(out[i[0]][1]) 
                 )  

################################################################################
#
# Drives the command line interface.
#    
################################################################################  
def commandLineInterface():
    print("""
Convert:

  1)   w/o   to   a/o
  2)   a/o   to   w/o
  3) a/bn-cm to   a/o
  4) a/bn-cm to   w/o 
  5)   w/o   to a/bn-cm
  6)   a/o   to a/bn-cm
""")
    
    i = raw_input("Which conversion (1-6)? ")
    i = int(i)

    if(i not in [1,2,3,4,5,6]):
        print("Invalid choice, valid choices are 1, 2, 3, 4, 5, or 6, exiting.")
        sys.exit(2)
    else:
        if(i == 1):
            (inp, bulk_density) = getInput("w/o")
            (out, bulk_density) = wo_to_ao(inp, bulk_density)
            printOutputTable(inp,"w/o","a/o",bulk_density,out)
        elif(i == 2):
            (inp, bulk_density) = getInput("a/o")
            (out, bulk_density) = ao_to_wo(inp, bulk_density)
            printOutputTable(inp,"a/o","w/o",bulk_density,out)
        elif(i == 3):
            (inp, bulk_density) = getInput("a/bn-cm")
            (out, bulk_density) = abncm_to_wo(inp, bulk_density)
            (out, bulk_density) = wo_to_ao(out, bulk_density)
            printOutputTable(inp,"a/bn-cm","a/o",bulk_density,out)
        elif(i == 4):
            (inp, bulk_density) = getInput("a/bn-cm")
            (out, bulk_density) = abncm_to_wo(inp, bulk_density)
            printOutputTable(inp,"a/bn-cm","w/o",bulk_density,out)
        elif(i == 5):
            (inp, bulk_density) = getInput("w/o")
            (out, bulk_density) = wo_to_abncm(inp, bulk_density)
            printOutputTable(inp,"w/o","a/bn-cm",bulk_density,out)
        elif(i == 6):
            (inp, bulk_density) = getInput("a/o")
            (out, bulk_density) = ao_to_wo(inp, bulk_density)
            (out, bulk_density) = wo_to_abncm(out, bulk_density)
            printOutputTable(inp,"a/o","a/bn-cm",bulk_density,out)

################################################################################ 
#
# Main program execution.
#
################################################################################ 
try:
    opts, args = getopt.getopt(sys.argv[1:],"hcf:g",
                                           ["help","cli","file=","gui"])
except getopt.GetoptError as err:
    print(str(err))
    print("Use NumberDensityConverter.py -h for help, exiting.")
    sys.exit(2)

if(len(sys.argv) == 1):
    commandLineInterface()
else:
    for opt, arg in opts:
        if(opt in ('-h', '--help')):
            printHelp()
        elif(opt in('-c', '-cli')):
            commandLineInterface()
        elif(opt in('-f', '-file')):
            print("Direct file not yet available, use STDIN, exiting.")
            sys.exit(2)
        elif(opt in ('-g', '-gui')):
            print("GUI not yet available, exiting.")
            sys.exit(2)
