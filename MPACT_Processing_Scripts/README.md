MPACT_Processing_Scripts
========================

These scripts are used to process files resulting from MPACT executions.
Generally, these scripts are *ad hoc* solutions to temporary problems; however,
some components are highly reusable (such as Visit plotting calls).

Execution Instructions for Visit
--------------------------------

On Linux, an execution line might look like:

```/opt/visit2_8_0.linux-x86_64/bin/visit -nowin -cli -s <script.py>```

or

```/home/jkulesza/SRC/VISIT/bin/visit -nowin -cli -s <script.py>```

On OSX, an execution line might look like:

```/Applications/VisIt.app/Contents/Resources/bin/visit -nowin -cli -s <script.py>```

MPACT_VTK_File_Plot_Negative_Qbar_By_Material.py
------------------------------------------------

This script will read a VTK file produced by MPACT and look for
iteratively-printed edits for qbar of the form ```qbarggg########``` where ggg
is the energy group number leftpadded with underscores and ######## is the
subiteration count leftpadded with underscores.

This script will then produce plots, by material (as specified in the script) of
negative source.  The plots will be pseudocolor plots with a maximum value of
zero and minimum corresponding to the minimum value in the region visible (i.e.,
the minimum that corresponds to the material being plotted).

MPACT_VTK_File_Find_Zero_Source.py
----------------------------------

This script will read a VTK file produced by MPACT and look for
iteratively-printed edits for qbar of the form ```qbarggg########``` where ggg
is the energy group number leftpadded with underscores and ######## is the
subiteration count leftpadded with underscores.

This script will then produce an ASCII table by energy group for each negative
component of the source (external, self-scatter, via transport cross section,
and total q-bar source) and by material which the negativity took place in.

**Note**: that for each energy group, if any iteration produced negativity it
will be produced here.  As such, it is possible that some negative component of
the source did not contribute to the negative total source.

The resulting table will look like
```
Running: cli2.8.0 -nowin -s MPACT_VTK_File_Find_Zero_Source.py
Running: viewer2.8.0 -noint -nowin -host 127.0.0.1 -port 5600
Length of material array: 4777
Operating on: simple_case_TCP0_47g-Pn_core_FSRmesh.vtk
Found: 
      0 negative external source entry
    472 negative scattering source entry
      0 negative total cross section entry
     32 negative total source entry
Total: 504 Entries
-----------------------------------------------------------------------------------------------------
|       Group       |     Neg Ext.      |  Neg. Self-Scat.  |   Neg. Sig-Tr.    |    Neg. Q-bar     |
-----------------------------------------------------------------------------------------------------
|         1         |                   |         3         |                   |         3         |
|         2         |                   |         3         |                   |         3         |
|         3         |                   |         3         |                   |         3         |
|         4         |                   |         3         |                   |         3         |
|         5         |                   |         3         |                   |                   |
|         6         |                   |         3         |                   |                   |
|         7         |                   |         3         |                   |                   |
.
.
.
|        47         |                   |         3         |                   |                   |
-----------------------------------------------------------------------------------------------------
```
