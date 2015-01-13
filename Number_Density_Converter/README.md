Number_Density_Converter
========================

This script is an interactive shell script to convert amongst weight fraction,
atom fraction, and atom density (a/bn-cm) using isotopic/elemental mass data
from MCNP6.  Due to licensing issues, those nuclear data is not available;
however, it can be easily created by those who are interested.

Execution Instructions
----------------------

Execute as ```python NumberDensityConverter.py``` and a menu should appear as

```
Convert:

  1)   w/o   to   a/o
  2)   a/o   to   w/o
  3) a/bn-cm to   a/o
  4) a/bn-cm to   w/o 
  5)   w/o   to a/bn-cm
  6)   a/o   to a/bn-cm

Which conversion (1-6)?
```

From here, all prompts and outputs are expected to be self-explanatory.

Required File: NuclearData.py
-----------------------------

An external file is needed which supplies the isotopic/elemental mass data.
Because of licensing concerns, these data cannot be provided.  However, the
format of the file is given as follows to allow an ambitious user to synthesize
his or her own file.

Within this file, Python dictionaries are used to store data for reference in
the main application.  The dictionaries are as follows:

* Masses = { ZAID : Mass in Atomic Mass Units}
  where ZAID (or **Z** **A** **ID**entification number) is used to uniquely
  identify isotopes/elements where it is of the form ZZZAAA with no leading
  zeroes.  As an example: U-235's ZAID is 92235.
* Full_Name = { "mnemonic" : ZAID}
  where "mnemonic" is how the user would like to refer to ZAID values (in a more
  natural way).  As an example: "Hydrogen-1" is an appropriate mnemonic for ZAID
  1001 and "Helium" is appropriate for ZAID 2000.
* Short_Name = { "mnemonic" : ZAID}
  where "mnemonic" in this case is an abbreviation.  Using the previous example,
  one might use "H-1" or "He".
* Names = { ZAID : "name" }
  where the name is now associated with a given ZAID regardless of what the user
  chose to specify the ZAID with.  This is used for output purposes

Example Execution
-----------------

An example execution might go as follows for natural enriched uranium:

```
Convert:

  1)   w/o   to   a/o
  2)   a/o   to   w/o
  3) a/bn-cm to   a/o
  4) a/bn-cm to   w/o 
  5)   w/o   to a/bn-cm
  6)   a/o   to a/bn-cm

Which conversion (1-6)? 1
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): U-235 0.7 

    ZAID   Species             Input (w/o)   
   92235   U-235               0.700000000   
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): U-238 99.3

    ZAID   Species             Input (w/o)   
   92235   U-235               0.700000000   
   92238   U-238              99.300000000   
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): 0
What is the material bulk density (g/cc)? 19.1

    ZAID   Species              Mass (amu)            Input (w/o)    Bulk Density (g/cc)           Output (a/o)   
   92235   U-235             ---.---------            0.700000000           19.100000000            0.007088914   
   92238   U-238             ---.---------           99.300000000           19.100000000            0.992911086 
```

An example execution might go as follows for 3 w/o enriched uranium:

```
Convert:

  1)   w/o   to   a/o
  2)   a/o   to   w/o
  3) a/bn-cm to   a/o
  4) a/bn-cm to   w/o 
  5)   w/o   to a/bn-cm
  6)   a/o   to a/bn-cm

Which conversion (1-6)? 1
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): U-235 3.0

    ZAID   Species             Input (w/o)   
   92235   U-235               3.000000000   
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): U-238 97.0

    ZAID   Species             Input (w/o)   
   92235   U-235               3.000000000   
   92238   U-238              97.000000000   
Enter ZAID, Short Name, or Long Name followed by the associated w/o value (enter 0 to finish): 0
What is the material bulk density (g/cc)? 19.1

    ZAID   Species              Mass (amu)            Input (w/o)    Bulk Density (g/cc)           Output (a/o)   
   92235   U-235             ---.---------            3.000000000           19.100000000            0.030372126   
   92238   U-238             ---.---------           97.000000000           19.100000000            0.969627874 
```

Alternatively, one could use the included input files to perform the computation.  These are simply executed as:

```
python NumberDensityConverter.py < file.inp
```
