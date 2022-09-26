"""
This script converts NeSys .xyz files containing in-brain coordinates
to MeshView JSON format (https://meshview.apps.hbp.eu/).
"""

import os
import json


def parse_xyz(fname):
    jsondata = []
    obj = {}
    triplets = []

    with open(fname,"r") as xyz:
        for line in xyz:
            line = line.strip()
            if line.startswith("SCALE"):
                scale = int(line[6:])

            elif line.startswith("#"):

                if triplets:               
                    obj["triplets"] = triplets
                    jsondata.append(obj)

                obj = {}
                triplets = []                
                obj["name"] = line[1:]
                obj["scale"] = scale                

            elif line.startswith("RGB"):
                obj["r"] = int(float(line.split()[1])*255)
                obj["g"] = int(float(line.split()[2])*255)
                obj["b"] = int(float(line.split()[3])*255)

            elif line == "":
                pass

            else:
                triplets.extend([float(a) for a in line.split(" ")])

    return(jsondata)


if __name__=='__main__':
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    xyzfiles = [f for f in os.listdir(os.getcwd()) if f.endswith(".xyz")]

    for file in xyzfiles:
        result = parse_xyz(file)
        with open(file.replace(".xyz",".json"),"w") as output:
            json.dump(result,output)
