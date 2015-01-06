
# IMPORT PACKAGES ##############################################################

import subprocess
import sys
import re

# DEFINE CONSTANTS #############################################################

MAXGRPS = 47

matdict = {}

#matdict[5]  = "mat_1_fuel"
#matdict[6]  = "mat_2_moderator"
#matdict[7]  = "mat_3_baffle"

matdict[6]  = "mat_1_fuel"
matdict[7]  = "mat_2_clad"
matdict[8]  = "mat_7_moderator"
matdict[9]  = "mat_39_gap"
 
# DEFINE FUNCTIONS #############################################################

# Parse VTK file to segregate negative source components.
def getlist(infile, scalar_str):
    cmd = r'grep "SCALARS ' + scalar_str + '" ' + infile + ' | cut -c 9-23'
    cmdout = subprocess.check_output(cmd,shell=True)
    cmdlist = cmdout.split('\n')
    while '' in cmdlist: cmdlist.remove('')  
    return cmdlist

# Get group number from label.
def getlabelgrp(label):
    return int(re.sub("_","",label[4:7]))

# Get iteration from label.
def getlabelitr(label):
    return int(re.sub("_","",label[7:]))

# Get final iteration entries from the list of negative source (or source
# components). 
def getsublist(inlist):
    listn = 0
    for n,i in enumerate(inlist):
        if(n < len(inlist) - 1):
            if(int(re.sub("_","",i[4:7])) >= int(re.sub("_","",inlist[n+1][4:7]))):
                listn = n + 1
    return inlist[listn:] 

# Check to determine if a given negative qbar entry is the converged (final
# iteration) value relative to another source component array.
def checkfinalentry(inlist,comparelist):
    finlist = []
    for i in inlist:
        lastiter = True
        for j in comparelist:
            # If the component of the source for a given group has a higher
            # iteration number than what is believed to be the last iteration of
            # the total source for that group, it is NOT the total source for
            # that group and should not be included.
            if(getlabelgrp(j) == getlabelgrp(i) and
               getlabelitr(j) >  getlabelitr(i)):
                lastiter = False
        if(lastiter):
            finlist.append(i)

    return finlist

# Parse VTK file to get array values.
def getarray(infile,arrayname):
    cmd = r"sed -e '1,/^LOOKUP_TABLE " + arrayname + "/d' -e '/^POINT_DATA/,$d' " + infile
    cmdout = subprocess.check_output(cmd,shell=True)
    array = cmdout.split()
    while '' in array: array.remove('')  
    return array

# EXECUTE PROGRAM ##############################################################

try:
    infile = sys.argv[1]
except:
    print "Error: No VTK file defined in ARGV"
    exit()
 
# Collect all VTK SCALAR entries corresponding to negative sources.
nextlist = getlist(infile,"next")
nssslist = getlist(infile,"nsss")
nstrlist = getlist(infile,"nstr")
qbarlist = getlist(infile,"qbar")

# Collect material listing into sorted list of integers.
matarray = sorted(set(getarray(infile,"material_table")))
matarray = map(int, matarray)

# Output general diagnostic information preceded by a delimiter.
print(80*"=")
print("Operating on file: " + infile)  

print("Found the following materials: " + " ".join(map(str,matarray)))
print("Found: ")
print("  " + "{:>5}".format(str(len(nextlist))) + " negative external source entry")
print("  " + "{:>5}".format(str(len(nssslist))) + " negative scattering source entry")
print("  " + "{:>5}".format(str(len(nstrlist))) + " negative total cross section entry")
print("  " + "{:>5}".format(str(len(qbarlist))) + " negative total source entry")
print("Total: " + str(len(nextlist)+len(nssslist)+len(nstrlist)+len(qbarlist)) + " Entries")

#if(len(nextlist) > 0): nextlist = getsublist(nextlist); print(nextlist)
#if(len(nssslist) > 0): nssslist = getsublist(nssslist); print(nssslist)
#if(len(nstrlist) > 0): nstrlist = getsublist(nstrlist); print(nstrlist)

if(len(qbarlist) > 0): 
    qbarlist = getsublist(qbarlist)
    # Check to ensure that qbar is truly last value for all iterations for a
    # given group.
    if(len(nextlist) > 0): qbarlist = checkfinalentry(qbarlist,nextlist) 
    if(len(nssslist) > 0): qbarlist = checkfinalentry(qbarlist,nssslist) 
    if(len(nstrlist) > 0): qbarlist = checkfinalentry(qbarlist,nstrlist) 
    print("Final Iteration Negative Sources: ")
    print(qbarlist)

# PERFORM VTK PLOTTING #########################################################

OpenDatabase("localhost:./" + infile, 0)

for qbar in qbarlist:

    print("Creating plot by material for: " + qbar)
    
    # Open the file.
    DeleteActivePlots()
    AddPlot("Pseudocolor", qbar, 1, 1)
     
    # Perform subset selection.
    silr = SILRestriction()
     
    # Set pseudocolor options.
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.limitsMode = PseudocolorAtts.CurrentPlot # OriginalData, CurrentPlot
    PseudocolorAtts.maxFlag = 1
    PseudocolorAtts.max = 0
    PseudocolorAtts.colorTableName = "Reds"
    PseudocolorAtts.invertColorTable = 1
    SetPlotOptions(PseudocolorAtts)
     
    # Set annotation options (turn off clutter).
    AnnotationAtts = AnnotationAttributes()
    
    AnnotationAtts.axes3D.autoSetTicks = 0
    
    AnnotationAtts.axes3D.xAxis.tickMarks.visible = 0
    AnnotationAtts.axes3D.yAxis.tickMarks.visible = 0
    AnnotationAtts.axes3D.zAxis.tickMarks.visible = 0
    
    AnnotationAtts.axes3D.xAxis.title.visible = 0
    AnnotationAtts.axes3D.xAxis.label.visible = 0
    AnnotationAtts.axes3D.yAxis.title.visible = 0
    AnnotationAtts.axes3D.yAxis.label.visible = 0
    AnnotationAtts.axes3D.zAxis.title.visible = 0
    AnnotationAtts.axes3D.zAxis.label.visible = 0
    
    AnnotationAtts.axes3D.triadFlag = 0
    AnnotationAtts.axes3D.bboxFlag = 1
    
    SetAnnotationAttributes(AnnotationAtts)          
    
    # Draw the plot. 
    DrawPlots()
     
    # Adjust view to be an orthogonal plan view.                                                                            
    View3DAtts = View3DAttributes()                                                                                         
    View3DAtts.viewNormal = (0, 0, 1)
    View3DAtts.focus = (39.264, 19.632, 0.5)
    View3DAtts.viewUp = (0, 1, 0)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 43.9013
    View3DAtts.nearPlane = -87.8027
    View3DAtts.farPlane = 87.8027
    View3DAtts.imagePan = (0, 0)
    View3DAtts.imageZoom = 1
    View3DAtts.perspective = 0
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (39.264, 19.632, 0.5)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
    SetView3D(View3DAtts)

    # Adjust the legend.
    plotName = GetPlotList().GetPlots(0).plotName 
    legend = GetAnnotationObject(plotName)

    legend.xScale = 3.
#   legend.yScale = 3.
#   legend.managePosition = 0
#   legend.position = (0.7,0.15)
    
    legend.orientation = legend.HorizontalBottom

    # For each material of interest.
    for mat in matdict:
    
        print("Operating on: " + matdict[mat])
    
        # Perform subset selection.
        silr = SILRestriction()
        silr.TurnOffAll()
        silr.TurnOnSet(mat) 
        SetPlotSILRestriction(silr ,1)
    
        # Perform query for minimum value in material.
        SetQueryFloatFormat("%g")
        matq = Query("MinMax", use_actual_data=1)
    
        print(matq)
    
        matqmin = float(re.search(r"Min = (.*?) ",matq).group(1))
    
        # If a negative value is found in that material, plot.
        if(matqmin < 0):
            print("Found negative source (" + str(matqmin) + ") in " + matdict[mat])
            SaveWindowAtts = SaveWindowAttributes()
            SaveWindowAtts.outputToCurrentDirectory = 1
            SaveWindowAtts.outputDirectory = "."
            SaveWindowAtts.fileName = infile + "_" + qbar + "_" + matdict[mat] + "_plot"
            SaveWindowAtts.family = 0
            SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY
            SaveWindowAtts.width = 2048
            SaveWindowAtts.height = 2048
            SaveWindowAtts.quality = 90
            SetSaveWindowAttributes(SaveWindowAtts)
            SaveWindow()
    
exit() 
