
# Call as 

# ... MPACT_VTK_File_Plot_Response.py file.vtk response material_number


# DEFINE CONSTANTS #############################################################
 
# DEFINE FUNCTIONS #############################################################

# VISIT function to make custom color tables.
def MakeRGBColorTable(name, ct):
    ccpl = ColorControlPointList()
    for pt in ct:
        p = ColorControlPoint()
        p.colors = (pt[0] * 255, pt[1] * 255, pt[2] * 255, 255)
        p.position = pt[3]
        ccpl.AddControlPoints(p)
    AddColorTable(name, ccpl)

# EXECUTE PROGRAM ##############################################################

try:
    infile = sys.argv[1]
except:
    print("Error: No VTK file defined in ARGV.")
    exit()

try:
    inresponse = sys.argv[2]
except:
    print("Error: No VTK response given.")
    exit()

try:
    inmaterial = sys.argv[3]
except:
    inmaterial = ""
    print("Warning: No VTK material given, showing all materials.")

OpenDatabase("localhost:./" + infile, 0)

print("Creating plot by material for: " + inresponse)

# Open the file.
DeleteActivePlots()
AddPlot("Pseudocolor", inresponse, 1, 1)

# Perform subset selection.
if(inmaterial): 
    silr = SILRestriction()

# Make a color table. each control point is: (r,g,b,t)
ct = ((1.000,1.000,1.000,0.000),          # Orig: (1.000,0.961,0.941,0.000)
      (0.996,0.878,0.824,0.125),
      (0.988,0.733,0.631,0.250),
      (0.988,0.573,0.447,0.375),
      (0.984,0.416,0.290,0.500),
      (0.937,0.231,0.173,0.625),
      (0.796,0.094,0.114,0.750),
      (0.647,0.059,0.082,0.875),
      (0.404,0.000,0.051,1.000))
MakeRGBColorTable("myreds", ct)
  
# Set pseudocolor options.
PseudocolorAtts = PseudocolorAttributes()
PseudocolorAtts.limitsMode = PseudocolorAtts.CurrentPlot # OriginalData, CurrentPlot
PseudocolorAtts.maxFlag = 1
PseudocolorAtts.max = 0
PseudocolorAtts.colorTableName = "myreds"
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

AnnotationAtts.databaseInfoFont.font = AnnotationAtts.databaseInfoFont.Arial  # Arial, Courier, Times
AnnotationAtts.databaseInfoFont.scale = 0.5

AnnotationAtts.userInfoFlag = 0
AnnotationAtts.timeInfoFlag = 0
 
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
#legend.yScale = 3.
#legend.managePosition = 0
#legend.position = (0.7,0.15)

legend.orientation = legend.HorizontalBottom

if(inmaterial):
    print("Operating on: " + inmaterial)
    
    # Perform subset selection.
    silr = SILRestriction()
    silr.TurnOffAll()
    silr.TurnOnSet(int(inmaterial))
    SetPlotSILRestriction(silr ,1)

SaveWindowAtts = SaveWindowAttributes()
SaveWindowAtts.outputToCurrentDirectory = 1
SaveWindowAtts.outputDirectory = "."
SaveWindowAtts.fileName = infile + "_" + inresponse + "_" + inmaterial + "_plot"
SaveWindowAtts.family = 0
SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY
SaveWindowAtts.width = 2048
SaveWindowAtts.height = 2048
SaveWindowAtts.quality = 90
SetSaveWindowAttributes(SaveWindowAtts)
SaveWindow()

exit() 
