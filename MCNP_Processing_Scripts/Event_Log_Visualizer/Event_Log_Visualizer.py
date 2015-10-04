# IMPORT PACKAGES ##############################################################

from lxml import etree
import math
import numpy as np
import sys
import re

# DEFINE CONSTANTS #############################################################



# DEFINE FUNCTIONS #############################################################

def write_VTP_file(outfilename, 
                   point_list, 
                   energy_list, 
                   weight_list, 
                   cell_list,
                   line_list,
                   connectivity_list, 
                   offset_list,
                   numLines):

    numPoints = str(len(point_list))
    numLines = str(numLines)

    vtpfile = etree.Element('VTKFile', type="PolyData", version="0.1", byte_order="LittleEndian")

    polydata = etree.SubElement(vtpfile, 'PolyData')

    piece = etree.SubElement(polydata, 'Piece', NumberOfPoints=numPoints, NumberOfVerts="0", NumberOfLines=numLines, NumberOfStrips="0", NumberOfPolys="0")
    
    pointdata = etree.SubElement(piece, 'PointData', Scalars="Scalars")
    dataarray = etree.SubElement(pointdata, 'DataArray', type="Float32", Name="energy", format="ascii")
    dataarray.text = ' '.join(energy_list)
    dataarray = etree.SubElement(pointdata, 'DataArray', type="Float32", Name="weight", format="ascii")
    dataarray.text = ' '.join(weight_list) 
    dataarray = etree.SubElement(pointdata, 'DataArray', type="Float32", Name="cell", format="ascii")
    dataarray.text = ' '.join(cell_list)

    celldata = etree.SubElement(piece, 'CellData', Scalars="Scalars")
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="line", format="ascii")
    dataarray.text = ' '.join(line_list) 
 

    points = etree.SubElement(piece, 'Points')
    dataarray = etree.SubElement(points, 'DataArray', type="Float32", NumberOfComponents="3", format="ascii")
    dataarray.text = ' '.join(point_list)
    
    lines= etree.SubElement(piece, 'Lines')
    dataarray = etree.SubElement(lines, 'DataArray', type="Float32", Name="connectivity", format="ascii")
    dataarray.text = ' '.join(connectivity_list)
    dataarray = etree.SubElement(lines, 'DataArray', type="Float32", Name="offsets", format="ascii")
    dataarray.text = ' '.join(offset_list)
  
    f = open(outfilename, 'w')
    f.write(etree.tostring(vtpfile, pretty_print=True).decode('UTF-8'))
    f.close() 

    return 

# Get information for a given state within an event log entry
def get_state_information(s):
    s = s.split(' ')
    s = filter(None, s)
    sd = {}
    sd['type'] = s[0]
    sd['cell'] = s[1]
    sd['x']    = s[2]
    sd['y']    = s[3]
    sd['z']    = s[4]
    sd['u']    = s[5]
    sd['v']    = s[6]
    sd['w']    = s[7]
    sd['erg']  = s[8]
    sd['wgt']  = s[9]

    for k,v in sd.iteritems():
        sd[k] = re.sub(r'(\d\.\d+)([+-]\d+)', '\g<1>e\g<2>', v)

    return(sd)

#########################

def extract_event_log(outp = '', rm_surf = True):

    event_list = re.findall(r'(event log for particle history no.*?)(?:\n \n|1problem)', outp, re.S)

    offset = 0
    numLines = 0

    point_list = []

    energy_list = []
    weight_list = []
    cell_list = []
    line_list = []

    connectivity_list = []
    offset_list = []

#   event_list = [event_list[0]]

    for e in event_list:
        e = e.split('\n')
        e = filter(None, e)
        e = [ x for x in e if "event log" not in x ]
        e = [ x for x in e if "cell" not in x ]
        if(rm_surf):
            e = [ x for x in e if "surf=" not in x ]

        line_start = len(point_list)

        for s in e:
            s_dict = get_state_information(s)
            pt = s_dict['x'] + ' ' + s_dict['y'] + ' ' + s_dict['z']
            point_list.append(pt)

            energy_list.append(s_dict['erg'])
            weight_list.append(s_dict['wgt'])
            cell_list.append(s_dict['cell'])

        line_list.append(str(numLines+1))

        line_stop = len(point_list)

        for c in range(line_start, line_stop + 1):
            connectivity_list.append(str(c))

        offset = offset + line_stop + 1 - line_start
        offset_list.append(str(offset))
        numLines = numLines + 1

    return(point_list, energy_list, weight_list, cell_list, line_list, connectivity_list, offset_list, numLines)

# EXECUTE PROGRAM ##############################################################

if __name__ == "__main__":

    try:
        infilename = sys.argv[1]
    except:
        print("Error: No MCNP outp file defined in ARGV")
        exit()
    
    with open (infilename, "r") as myfile:
        outp = myfile.read()


    point_list, energy_list, weight_list, cell_list, line_list, connectivity_list, offset_list, numLines = extract_event_log(outp) 

    write_VTP_file(infilename + '.vtp', 
                   point_list, 
                   energy_list, 
                   weight_list, 
                   cell_list,
                   line_list,
                   connectivity_list, 
                   offset_list,
                   numLines)

