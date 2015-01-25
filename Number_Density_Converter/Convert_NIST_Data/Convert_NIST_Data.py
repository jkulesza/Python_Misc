
import re

with open ("NIST_Masses.dat", "r") as f:
    masses = f.read()

# Remove uncertainty information.
masses = re.sub("\(.*?\)","",masses)
masses = re.sub("\#","",masses)
masses = re.sub("\[","",masses)
masses = re.sub("\]","",masses)

# Remove extraneous fields.
masses = re.sub("Atomic Symbol = .*?\n","",masses)
masses = re.sub("Isotopic Composition = .*?\n","",masses)
masses = re.sub("Notes = .*?\n","",masses)

# Remove header.
masses = re.sub("Atomic Weights and Isotopic Compositions.*?\n","",masses)
masses = re.sub("Description of Quantities and Notes","",masses)

# Remove footer.
masses = re.sub("NIST \| Physical Measurement Laboratory.*?\n","",masses)

# Convert to tabular layout.
masses = re.sub("\n\n","|\n",masses)
masses = re.sub("\n",",",masses)
masses = re.sub("\|","\n",masses)

# Reduce all lines with spaces to be without spaces.
masses = re.sub("\n,","\n",masses)

# Split table into rows.
masses = masses.split("\n")

# Remove empty entries.
masses = filter(None, masses)

final_masses = []
# Process each entry.
for m in masses:
    # Get Z and A numbers.
    Z = int(re.search("Atomic Number = (\d+)", m).group(1))
    A = int(re.search("Mass Number = (\d+)", m).group(1))
    
    # Try to get isotopic mass.
    try:
        mass_iso = float(re.search("Relative Atomic Mass = (\d+\.*\d*)", m).group(1)) 
    except:
        mass_iso = 0.0

    # Try to get elemental mass.    
    try:
        mass_ele = float(re.search("Standard Atomic Weight = (\d+\.*\d*)", m).group(1)) 
    except:
        mass_ele = 0.0

    ZAID = Z * 1000 + A

    # Print summary values. 
#   print("{0:>3n} {1:>3n} {2:>6n} {3:6.4e} {4:6.4e}".format(Z,A,ZAID,mass_iso,mass_ele))

    if(mass_iso != 0.0):
        final_masses.append((ZAID, mass_iso))
    final_masses.append((Z * 1000, mass_ele))

final_masses = sorted(set(final_masses))
for m in final_masses:
    print(str(m[0]) + " : " + str(m[1]) + ",")
