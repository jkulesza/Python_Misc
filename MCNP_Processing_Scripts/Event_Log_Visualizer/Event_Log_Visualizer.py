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
                   history_list,
                   track_list,
                   connectivity_list, 
                   offset_list,
                   joinStr = '\n          '):

    numPoints = str(len(point_list))
    numLines = str(len(connectivity_list))

    vtpfile = etree.Element('VTKFile', type="PolyData", version="0.1", byte_order="LittleEndian")

    polydata = etree.SubElement(vtpfile, 'PolyData')

    piece = etree.SubElement(polydata, 'Piece', NumberOfPoints=numPoints, NumberOfVerts="0", NumberOfLines=numLines, NumberOfStrips="0", NumberOfPolys="0")
    
    celldata = etree.SubElement(piece, 'CellData', Scalars="Scalars")
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="energy", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(energy_list) + '\n        '
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="weight", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(weight_list) + '\n        '
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="cell", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(cell_list) + '\n        '
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="history", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(history_list) + '\n        '
    dataarray = etree.SubElement(celldata, 'DataArray', type="Float32", Name="track", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(track_list) + '\n        '

    points = etree.SubElement(piece, 'Points')
    dataarray = etree.SubElement(points, 'DataArray', type="Float32", NumberOfComponents="3", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(point_list) + '\n        '
    
    lines= etree.SubElement(piece, 'Lines')
    dataarray = etree.SubElement(lines, 'DataArray', type="Float32", Name="connectivity", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(connectivity_list) + '\n        '
    dataarray = etree.SubElement(lines, 'DataArray', type="Float32", Name="offsets", format="ascii")
    dataarray.text = '\n          ' + joinStr.join(offset_list) + '\n        '
  
    f = open(outfilename, 'w')
    f.write(etree.tostring(vtpfile, pretty_print=True).decode('UTF-8'))
    f.close() 

    return 

# Get information for a given state within an event log entry
def get_state_information(s):
    s = s.split(' ')
    s = list(filter(None, s))
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

    for k,v in sd.items():
        sd[k] = re.sub(r'(\d\.\d+)([+-]\d+)', '\g<1>e\g<2>', v)

    return(sd)

#########################

def extract_event_log(outp = ''):

    event_list = re.finditer(r'(?=(1\s+event log.*?)\n1)', outp, re.S)
    event_list = [event.group(1) for event in event_list]

    segment = 0
    offset = 0
    numLines = 0

    point_list = []

    energy_list = []
    weight_list = []
    cell_list = []
    history_list = []
    line_list = []

    connectivity_list = []
    offset_list = []

    for e in event_list:

        history = re.search(r'no\.\s+(\d+)\s+', e).group(1)
        track = 0
        print('Found event log entry for history ' + history + '.')

        # Remove print table 110 entries.
        e = re.sub(r'\n\s+\d+\s+.*$', '', e, re.M)
        e = re.sub(r'\n\s+', r'\n', e)
        e = re.sub(r'^.*?event log.*?\n', '', e, re.S)
        e = re.sub(r'^.*?cell.*?\n', '', e, re.S)
        e = re.sub(r'\s+\n+$', '', e, re.S)

        # Find original and bank tracks in each history.        
        track_list = re.finditer(r'(?=((?:source|bank).*?ter.*?)(?:\n|$))', e, re.S)
        track_list = [track.group(1) for track in track_list]

        for t in track_list:
            track = track + 1
            print('Processing track ' + str(track) + '.')

            for n, s in enumerate(t.split('\n')):
                s_dict = get_state_information(s)
                pt = s_dict['x'] + ' ' + s_dict['y'] + ' ' + s_dict['z']
    
                point_list.append(pt)
                if(n != len(t)-1):
                    energy_list.append(s_dict['erg'])
                    weight_list.append(s_dict['wgt'])
                    cell_list.append(s_dict['cell'])
                    history_list.append(str(history))
                    line_list.append(str(track))
                    connectivity_list.append(str(segment) + ' ' + str(segment + 1))
                    segment = segment + 1
                    offset = offset + 2
                    offset_list.append(str(offset))

    return(point_list, energy_list, weight_list, cell_list, history_list, line_list, connectivity_list, offset_list)

# EXECUTE PROGRAM ##############################################################

if __name__ == "__main__":

    try:
        infilename = sys.argv[1]
    except:
        print("Error: No MCNP outp file defined in ARGV")
        exit()
    
    with open (infilename, "r") as myfile:
        outp = myfile.read()


    point_list, energy_list, weight_list, cell_list, history_list, track_list, connectivity_list, offset_list = extract_event_log(outp) 

    write_VTP_file(infilename + '.vtp', 
                   point_list, 
                   energy_list, 
                   weight_list, 
                   cell_list,
                   history_list,
                   track_list,
                   connectivity_list, 
                   offset_list)

