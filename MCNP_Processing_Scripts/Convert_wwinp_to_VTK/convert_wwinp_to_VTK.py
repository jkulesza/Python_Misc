# IMPORT PACKAGES ##############################################################

import numpy as np
import sys
import re

# DEFINE CONSTANTS #############################################################



# DEFINE FUNCTIONS #############################################################

# Create a linearly-interpolated spatial mesh array in 1D based on the wwinp
# start, mesh, and end lines.  Note that this does not take account of
# coarse/fine mesh in wwinp - it assumes the user stretched one coarse mesh over
# the whole problem.
def create_1D_spatial_mesh(dim_array):
    i = list(filter(None, dim_array.split(' ')))
    imin =     float(i[0])
    ni   = int(float(i[1]))
    imax =     float(i[2])
    idel = ni + 0
    i = np.linspace(imin, imax, idel)
    return(ni, i)

# Create an array listing the energy mesh from the wwinp file.
def create_1D_energy_mesh(erg_array):
    i = [float(i) for i in (list(filter(None, erg_array.split(' '))))]
    i = np.array(i)
    ni = len(i)
    return(ni, i)
 
# Split apart wwinp file to extract key header data.  This was done *very* 
# quickly, and badly.  It works for cases with only one coarse mesh in one
# direction and one energy group.  However, the word is: works.
def extract_wwinp_data(wwinp):

    # Split the file using hard boundaries - stupid, but fast.
    wwinp = wwinp.split('\n')

    # Get number of mesh and mesh boundaries.
    nx, x = create_1D_spatial_mesh(wwinp[4])
    ny, y = create_1D_spatial_mesh(wwinp[5])
    nz, z = create_1D_spatial_mesh(wwinp[6])
    ne, e = create_1D_energy_mesh(wwinp[7])

    # Split ww value array into list of individual values.
    ww = wwinp[8:]
    ww = " ".join(ww)
    ww = re.sub(r'\s+', ' ', ww)
    ww = ww.split(' ')
    ww = [float(i) for i in list(filter(None, ww))]
    ww = np.array(ww)

    # Very basic error checking.
    if(len(ww) != ne * nx * ny * nz):
        raise ValueError('Incorrect number of weight window values versus \
spatial mesh.')

    return (nx, ny, nz, ne), (x, y, z, e), ww

# Reformat a vector of data into a table of values, formatted consistently.
def print_table_of_values(vec, cols, fmt):
    table = ""
    for n, i in enumerate(vec):
        if(fmt == 'Int'):
            table += ' {:13d}'.format(i)
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
def create_Cartesian_VTK(outfilename, nx, ny, nz, ne, x, y, z, e, ww):

    minval = str(np.min(ww[np.nonzero(ww)]))

    f = open(outfilename, 'w')

    f.write('# vtk DataFile Version 2.0\n')
    f.write('MCNP Weight Window Input File; Minimum Non-Zero Value: ' + minval + '\n')
    f.write('ASCII\n')
    f.write('DATASET RECTILINEAR_GRID\n')
    f.write('DIMENSIONS ' + str(nx) + ' ' + str(ny) + ' ' + str(nz) + '\n')

    f.write('X_COORDINATES ' + str(nx) + ' float\n')
    f.write(print_table_of_values(x, 5, 'Float'))

    f.write('Y_COORDINATES ' + str(ny) + ' float\n')
    f.write(print_table_of_values(y, 5, 'Float'))

    f.write('Z_COORDINATES ' + str(nz) + ' float\n')
    f.write(print_table_of_values(z, 5, 'Float'))

    ww = np.split(ww, ne)

    f.write('POINT_DATA ' + str(nx * ny * nz) + '\n')
    for n, i in enumerate(e):
        erg = '{:5.3e}'.format(i)
        f.write('SCALARS Weight_Windows_Upper_Erg_' + erg + ' float\n')     
        f.write('LOOKUP_TABLE Weight_Windows_Upper_Erg_' + erg + '_table\n')     
#       f.write('LOOKUP_TABLE default\n')
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

(nx, ny, nz, ne), (x, y, z, e), ww = extract_wwinp_data(wwinp)

create_Cartesian_VTK(   outfilename = infilename + '.vtk',
                        nx = nx, ny = ny, nz = nz, ne = ne,
                        x = x, y = y, z = z, e = e, ww = ww)
