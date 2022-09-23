"""
This script converts NeSys .xyz files with coordinates specified
in the local coordinate system for the pontine nuclei defined by
Leergaard et al. 2000 to Waxholm Space coordinates for the rat brain
(in voxels).
"""
# pylint: disable=C0103
import os
import random
random.seed()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Function definitions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def listXYZfiles(folder):
    r"""This function selects non-WHS .xyz files from the active folder,
    and returns the list of file names"""
    filelist = []

    for file in os.listdir(folder):
        if file.endswith(".xyz"):
            if file.endswith("-WHSvox.xyz"):
                pass
            else:
                filelist.append(file)

    print("Found " + str(len(filelist)) + " non-WHS .xyz files to convert.")
    return filelist

def convert(ponscoords):
    r"""This function converts incoming coordinates defined in the pontine
    nuclei local coordinate system to rat brain Waxholm Space coordinates (in voxels)"""
    WHScoords = []
    WHScoords.append(0.00)
    WHScoords.append(0.00)
    WHScoords.append(0.00)

    WHScoords[0] = 244 + float(ponscoords[0])/2000*59.5
    WHScoords[1] = 429.9371725 + float(ponscoords[2])/2000*-47.2076 + float(ponscoords[1])/1200*10.99089
    WHScoords[2] = 188.2860875 + float(ponscoords[2])/2000*-36.3546 + float(ponscoords[1])/1200*-16.2843
    
    return WHScoords

def rndRGB():
    R=1
    G=1
    B=1
    while (R+G+B)>2.5: # Get darker colors
        R = random.randint(0,255)/255
        G = random.randint(0,255)/255
        B = random.randint(0,255)/255

    RGBline = "RGB " + str(R) + " " + str(G) + " " + str(B) + "\n"
    return RGBline

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Program core
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Define max. nr of points in one rendering group for MeshView
GROUP_SIZE = 8000

# Initialize point counter (max. size: GROUP_SIZE)
pointcounter = 0

# Remember color settings for point groups larger than GROUP_SIZE
# groupcolor = "RGB 1 0 0\n" # Default color: Red

# Get list of .xyz files in the current folder
os.chdir(os.path.dirname(os.path.realpath(__file__)))
xyzfiles = listXYZfiles(os.getcwd())

# Take each file on the list:
for file in xyzfiles:

    groupcolor = rndRGB()
    
    # Open pons file for reading
    ponsfile = open(file, "r")

    # Create WHS file for writing
    newfilename = file[:-4] + "-WHSvox-sameRGB.xyz"
    WHSfile = open(newfilename, "w")
    WHSfile.write("SCALE 5\n")

    # Parse file
    for line in ponsfile:

        if line.startswith("#"):                    # New point group starts
            pointcounter = 0                        # Reset point counter
            WHSfile.write(line)                     # Comments: copy as they are
            # groupcolor = rndRGB()                   # Reset group color
            WHSfile.write(groupcolor)               # Add RGB color for MeshView
        elif not line.strip():                      # Empty line (only spaces)
            WHSfile.write("\n")
        else:
            pointcounter += 1
            if pointcounter==GROUP_SIZE+1:
                WHSfile.write(groupcolor)           # Start new rendering group for MeshView, but keep old colors
                pointcounter=1
            # Convert coordinates
            newcoords = convert(line.split())
            # Write new coordinates to file
            WHSfile.write(str(newcoords[0]) + " " + str(newcoords[1]) + " " + str(newcoords[2]) + "\n")

    # Close both files
    ponsfile.close()
    WHSfile.close()

print("Conversion complete.")
