
# coding: utf-8

## Initialization

# In[38]:

get_ipython().run_cell_magic(u'html', u'', u"<style>\ndiv.input {\nwidth: 105ex; /* about 80 chars + buffer */\n}\n \ndiv.text_cell {\nwidth: 105ex /* instead of 100%, */\n}\n \ndiv.text_cell_render {\n/*font-family: sans-serif;*/\nfont-family: serif; /* Make non-code text serif. */\nline-height: 145%; /* added for some line spacing of text. */\nwidth: 105ex; /* instead of 'inherit' for shorter lines */\n}\n \n/* Set the size of the headers */\ndiv.text_cell_render h1 {\nfont-size: 18pt;\n}\n \ndiv.text_cell_render h2 {\nfont-size: 14pt;\n}\n \n.CodeMirror {\nfont-family: monospace;\n}\n</style>")


# In[39]:

get_ipython().run_cell_magic(u'javascript', u'', u'IPython.OutputArea.auto_scroll_threshold = -1;')


# In[40]:

#
# Initialize Environment
#
get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as tf
#
import glob
import math
import numpy as np
import re
import sys
#
figuresize = 8
plt.rcParams['figure.figsize'] = (1+math.sqrt(5))/2*figuresize, figuresize
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 16
plt.rcParams['font.family'] = "serif"
plt.rcParams['text.usetex'] = "True"


# In[41]:

# Validate that width of environment is 80 characters.
for j in range(1,9):
    sys.stdout.write(9*" " + str(j))
sys.stdout.write("\n")
for i in range(1,81):
    sys.stdout.write(str(i)[-1])


## Function Definitions

# In[42]:

#
# Function to read ULTRA file.
#   Parameter(s): ULTRA data file location & name.
#   Returns: Curve-wise list of data with x & y lists for each curve.
#
def read_ULTRA_file(filename):

    # Read ULTRA file contents.
    with open (filename, "r") as infile:
        alldata = infile.read()

    # Split contents on standard VISIT header for each data set.
    tmpdata = re.split("#\s+curve\d+",alldata)

    # Split contents into x,y lists and remove null entries throughout.
    data = []
    for i,d in enumerate(tmpdata):
        #print("Processing data set " + str(i+1) + ".")
        tmp = filter(None, d.split("\n"))
        data.append(tmp)

    data = filter(None,data)

    tmpdata = data; data = []
    for i,m in enumerate(tmpdata):
        x = []
        y = []
        for j,n in enumerate(m):
            tmpx,tmpy = n.split()
            x.append(tmpx)
            y.append(tmpy)
        data.append([x,y])

    return(data)


## Workflow Execution

# In[43]:

#
# Read ULTRA data file into variable 'data'.
#
data = read_ULTRA_file("/Users/jkulesza/tmp/simple_case_data_flux_all.ultra")   


# In[44]:

#
# Set geometry information.
#
start_fuel = 0.0
width_fuel = 17 * 1.26

start_baffle = width_fuel
width_baffle = 2 * 1.26

start_reflector = width_fuel + width_baffle
width_reflector = 34 * 1.26 - (start_reflector)


# In[45]:

#
# Create plot of group data for all groups.
#
fig = plt.figure()
ax = fig.add_subplot(111)

for i,d in enumerate(data):
    ax.plot(d[0], d[1], 'k-');


plt.title(r"Group-wise Neutron Flux versus Distance Along $x$ (All Groups)");
plt.xlabel(r"$x$ (cm)");
plt.ylabel(r"Group Neutron Flux (cm$^{-2}\cdot$s$^{-1}$)");

# Define transformation to use x coordinates as absolute and y coordinates 
# as relative.
trans = tf.blended_transform_factory(ax.transData, ax.transAxes)

patch = []

# Create rectangular zone to denote fuel region.
patch.append(patches.Rectangle((start_fuel,0), width=width_fuel, 
    height=1, transform=trans, color='red', alpha=0.05))

# Create a set of pins within the fuel region.
for i in range(0,17):
    patch.append(patches.Rectangle((i*1.26+(1.26-1.08)/2,0), width=1.08, 
        height=1, transform=trans, color='red', alpha=0.05))

# Create rectangular zone to denote baffle region.
patch.append(patches.Rectangle((start_baffle,0), width=width_baffle, 
    height=1, transform=trans, color='gray', alpha=0.05))

# Create rectangular zone to denote reflector region.
patch.append(patches.Rectangle((start_reflector,0), width=width_reflector, 
    height=1, transform=trans, color='blue', alpha=0.05))

for i,p in enumerate(patch):
    ax.add_patch(p)

plt.show();
#plt.savefig('tex_demo.pdf')


# In[46]:

#
# Create plot of group data for each group.
#
for i,d in enumerate(data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(d[0], d[1], 'k-');

    plt.title(r"Group-wise Neutron Flux versus Distance Along $x$ (Group " 
        + str(i+1) + ")");

    plt.xlabel(r"$x$ (cm)");

    plt.ylabel(r"Group " + str(i+1) 
        + " Neutron Flux (cm$^{-2}\cdot$s$^{-1}$)");

    # Define transformation to use x coordinates as absolute and y 
    # coordinates as relative.
    trans = tf.blended_transform_factory(ax.transData, ax.transAxes)

    patch = []

    # Create rectangular zone to denote fuel region.
    patch.append(patches.Rectangle((start_fuel,0), width=width_fuel, 
        height=1, transform=trans, color='red', alpha=0.05))
    
    # Create a set of pins within the fuel region.
    for i in range(0,17):
        patch.append(patches.Rectangle((i*1.26+(1.26-1.08)/2,0), width=1.08, 
            height=1, transform=trans, color='red', alpha=0.05))

    # Create rectangular zone to denote baffle region.
    patch.append(patches.Rectangle((start_baffle,0), width=width_baffle, 
        height=1, transform=trans, color='gray', alpha=0.05))

    # Create rectangular zone to denote reflector region.
    patch.append(patches.Rectangle((start_reflector,0), width=width_reflector, 
        height=1, transform=trans, color='blue', alpha=0.05))

    for i,p in enumerate(patch):
        ax.add_patch(p)

    plt.show();


# In[46]:



