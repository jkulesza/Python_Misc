# IMPORT PACKAGES ##############################################################

import math
import numpy as np
import sys
import re

# DEFINE CONSTANTS #############################################################



# DEFINE FUNCTIONS #############################################################

# Create a linearly-interpolated spatial mesh array in 1D based on the wwinp
# start, mesh, and end lines.
def create_1D_spatial_mesh(nc, nf, dim_array):
    dim_array = ' '.join(dim_array)
    dim_array = list(filter(None, dim_array.split(' ')))

    # Set basis of dimension.
    i0 = [float(dim_array.pop(0))]

    # Create dimension list.
    i = []
    i.append(i0)
    my_nf = 0
    for n in range(0,nc):
        ni   = int(float(dim_array[n*3+0]))
        imax = float(dim_array[n*3+1])
        i.append(np.linspace(i[n][-1], imax, ni+1))
        my_nf += ni

    i = [item for sublist in i for item in sublist]
    i = np.sort(np.array(list(set(i))))

    if(my_nf != nf or len(i)-1 != nf):
        raise ValueError('Unexpected number of fine spatial mesh ( ' + \
str(nf) + ' expected; ' + str(my_nf) + ' found with list length ' + str(len(i)) \
+ ')')

    return(i)

# Create an array listing the energy mesh from the wwinp file.
def create_1D_energy_mesh(ne, erg_array):
    erg_array = ' '.join(erg_array)
    e = [float(e) for e in (list(filter(None, erg_array.split(' '))))]
    e = np.array(e)
    my_ne = len(e)

    if(my_ne != ne or len(e) != ne):
        raise ValueError('Unexpected number of energy mesh')

    return(e)

# Get the range of lines in the wwinp file that define the various mesh / block
# boundaries.
def get_mesh_definition_range(nxc, nyc, nzc, ne):
    xr = []; yr = []; zr = []; er = []; wr = []

    # Determine lines of the wwinp file that various information falls on.
    xr.append(4)
    xr.append(xr[0] + int(math.ceil(nxc * 4 / 6))-1)
    yr.append(xr[1] + 1)
    yr.append(yr[0] + int(math.ceil(nyc * 4 / 6))-1)
    zr.append(yr[1] + 1)
    zr.append(zr[0] + int(math.ceil(nzc * 4 / 6))-1)
    er.append(zr[1] + 1)
    er.append(er[0] + int(math.ceil(ne  * 1 / 6))-1)
    wr.append(er[1] + 1)

    return xr, yr, zr, er, wr

# Split apart wwinp file to extract key header data.
def extract_wwinp_data(wwinp):

    # Split the file using hard boundaries - stupid, but fast.
    wwinp = wwinp.split('\n')

    # Get number of energy groups.
    ne = int(list(filter(None, wwinp[1].split(' ')))[0])

    # Get number of fine mesh in each dimension.
    fine_mesh = list(filter(None, wwinp[2].split(' ')))
    nxf = int(float(fine_mesh[0]))
    nyf = int(float(fine_mesh[1]))
    nzf = int(float(fine_mesh[2]))

    # Get number of coarse mesh in each dimension.
    coarse_mesh = list(filter(None, wwinp[3].split(' ')))
    nxc = int(float(coarse_mesh[0]))
    nyc = int(float(coarse_mesh[1]))
    nzc = int(float(coarse_mesh[2]))

    # Get dimension line ranges for the wwinp file.
    xr, yr, zr, er, wr = get_mesh_definition_range(nxc, nyc, nzc, ne)

    # Get number of mesh and mesh boundaries.
    x = create_1D_spatial_mesh(nxc, nxf, wwinp[xr[0]:xr[1]+1])
    y = create_1D_spatial_mesh(nyc, nyf, wwinp[yr[0]:yr[1]+1])
    z = create_1D_spatial_mesh(nzc, nzf, wwinp[zr[0]:zr[1]+1])
    e = create_1D_energy_mesh(ne, wwinp[er[0]:er[1]+1])

    # Split ww value array into list of individual values.
    ww = wwinp[wr[0]:]
    ww = " ".join(ww)
    ww = re.sub(r'\s+', ' ', ww)
    ww = ww.split(' ')
    ww = [float(i) for i in list(filter(None, ww))]
    ww = np.array(ww)

    # Very basic error checking.
    if(len(ww) != ne * nxf * nyf * nzf):
        raise ValueError('Incorrect number of weight window values versus \
spatial mesh.')

    return (nxf, nyf, nzf, ne), (x, y, z, e), ww

# Reformat a vector of data into a table of values, formatted consistently.
def print_table_of_values(vec, cols, fmt):
    table = ""
    for n, i in enumerate(vec):
        if(fmt == 'Int'):
            table += ' {:8d}'.format(i)
        elif(fmt == 'Float'):
            table += ' {:13.5e}'.format(i)
        else:
            raise ValueError('Unrecognized format.')

        if((n+1) % cols == 0):
            table += '\n'

    if(not re.search(r'\n$', table, re.S)):
        table += '\n'

    return table

# Create a Cartesian VTK file from key wwinp parameters and the ww distribution.
def create_Cartesian_VTK(outfilename, nxf, nyf, nzf, ne, x, y, z, e, ww):

    minval = str(np.min(ww[np.nonzero(ww)]))

    f = open(outfilename, 'w')

    # Print minimum non-zero weight window value for log-scaling purposes.
    print("Minimum non-zero value: " + minval)

    # Write VTK header information.
    f.write('# vtk DataFile Version 2.0\n')
    f.write('MCNP Weight Window Input File; Minimum Non-Zero Value: ' + minval + '\n')
    f.write('ASCII\n')
    f.write('DATASET RECTILINEAR_GRID\n')
    f.write('DIMENSIONS ' + str(nxf+1) + ' ' + str(nyf+1) + ' ' + str(nzf+1) + '\n')

    # Write VTK coordinate information.
    f.write('X_COORDINATES ' + str(nxf+1) + ' float\n')
    f.write(print_table_of_values(x, 5, 'Float'))
    f.write('Y_COORDINATES ' + str(nyf+1) + ' float\n')
    f.write(print_table_of_values(y, 5, 'Float'))
    f.write('Z_COORDINATES ' + str(nzf+1) + ' float\n')
    f.write(print_table_of_values(z, 5, 'Float'))

    # Write VTK data delimiter-like line.
    f.write('CELL_DATA ' + str(nxf * nyf * nzf) + '\n')

    # Output weight window mesh cell index.
    f.write('SCALARS Weight_Window_Mesh_Index int\n')
    f.write('LOOKUP_TABLE Weight_Window_Mesh_Index_table\n')
    f.write(print_table_of_values(range(1, nxf * nyf * nzf + 1), 10, 'Int'))

    # Split the whole weight window mesh into an array of the energy-grouped values.
    ww = np.split(ww, ne)

    # Output energy-grouped weight window values.
    for n, i in enumerate(e):
        erg = '{:5.3e}'.format(i)
        f.write('SCALARS Weight_Windows_Upper_Erg_' + erg + ' float\n')
        f.write('LOOKUP_TABLE Weight_Windows_Upper_Erg_' + erg + '_table\n')
        f.write(print_table_of_values(ww[n], 5, 'Float'))

    f.close()

    return

# EXECUTE PROGRAM ##############################################################

try:
    infilename = sys.argv[1]
except:
    print("Error: No MCNP wwinp file defined in ARGV")
    exit()

with open (infilename, "r") as myfile:
    wwinp = myfile.read()

(nxf, nyf, nzf, ne), (x, y, z, e), ww = extract_wwinp_data(wwinp)

create_Cartesian_VTK(   outfilename = infilename + '.vtk',
                        nxf = nxf, nyf = nyf, nzf = nzf, ne = ne,
                        x = x, y = y, z = z, e = e, ww = ww)
