"""
Left-right flip for point clouds represented as
WHS SD rat coordinate triplets in MeshView JSON format

"""

import json
import os

if __name__=='__main__':

    print('\nLeft-right flip for point clouds represented as WHS SD rat coordinate triplets in MeshView JSON format\n---')
    folder = input('Folder with JSON files: ')
    if not os.path.exists(folder):
        print('\nPath not found.\n')
        raise SystemExit
    files = os.listdir(folder)

    for file in files:
        if file.endswith('.json'):
            file = os.path.join(folder, file)
            jdict = json.load(open(file,'r'))[0]
            coords = jdict['triplets']
            flipped = []

            for i in range(0, len(coords)-3+1, 3):
                triplet = coords[i:i+3]
                x_flipped = 488 - triplet[0]
                flipped.extend([x_flipped, triplet[1], triplet[2]])

            jdict.update({'triplets':flipped})
            json.dump([jdict],open(file[:-5] + '_LRflipped.json','w'),indent=4)
