"""
This script flattens NeSys .xyz files containing in-brain coordinates.
"""

import os


def flatten_xyz(fname):
    result = ["RGB 0 0 0\n"]

    with open(fname,"r") as xyz:
        for line in xyz:
            if not (line.startswith("SCALE") or line.startswith("#") or line.startswith("RGB") or line.strip() == ""):
                result.append(line)

    return(result)


if __name__=='__main__':
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    xyzfiles = [f for f in os.listdir(os.getcwd()) if f.endswith(".xyz")]

    for file in xyzfiles:
        result = flatten_xyz(file)
        with open(file.replace(".xyz",".txt"),"w") as output:
            for line in result:
                output.write(line)
