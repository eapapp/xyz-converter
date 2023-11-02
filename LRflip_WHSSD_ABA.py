"""
Left-right flip for point clouds represented as WHS SD rat
and ABA mouse coordinate triplets in MeshView JSON format
and anchoring vectors in QuickNII JSON or XML format.

"""

import json
import os
import re

rat = False


def flip_json_anchors(coords):

    flipped = []

    for i in range(0, len(coords)-3+1, 3):
        triplet = coords[i:i+3]
        x_flipped = 488 - triplet[0] if rat else 456 - triplet[0]
        flipped.extend([x_flipped, triplet[1], triplet[2]])

    return(flipped)


def flip_xml_anchors(line):
    # Parse and LR flip anchoring vectors from QuickNII XML

    beginning, ending = line.split("anchoring='") 
    snippets = re.split("=|&", ending)
    ox = float(snippets[1])
    oy = float(snippets[3])
    oz = float(snippets[5])
    ux = float(snippets[7])
    uy = float(snippets[9])
    
    uz = float(snippets[11])
    vx = float(snippets[13])

    ox = 488 - ox if rat else 456 - ox
    ux = - ux
    vx = - vx

    flipped = beginning + "anchoring='" + snippets[0] + '=' + str(ox) + '&' + snippets[2] + '=' + str(oy) + '&' + snippets[4] + '=' + str(oz) + '&' + snippets[6] + '=' + str(ux) + '&' + snippets[8] + '=' + str(uy) + '&' + snippets[10] + '=' + str(uz) + '&' + snippets[12] + '=' + str(vx) + '&' + snippets[14] + '=' + snippets[15] + '&' + snippets[16] + '=' + snippets[17]

    return(flipped)


if __name__=='__main__':

    print('\nLeft-right flip for point clouds represented as WHS SD rat or ABA mouse coordinate triplets in MeshView JSON, QuickNII JSON, or QuickNII XML format\n---')
    print('This script looks for JSON and XML files in a folder and all of its subfolders and processes them either as rat or mouse.\nYou need to pre-select the species and all files in the selected folder will be processed accordingly. Therefore if you\nhave mixed data, please place them in separate folders (one for mouse and one for rat) and run the script separately for each.\n---')

    folder = input('Path to folder with JSON and/or XML files: ')
    if not os.path.exists(folder):
        print('\nPath not found.\n')
        raise SystemExit

    species = ''
    print('\nSelect species:')
    print('1. Mouse')
    print('2. Rat\n---')

    while not species:
        species = input('Species: ')
        if not species: raise SystemExit
        if not (species.strip() == '1' or species.strip() == '2'): species = ''

    rat = True if species.strip() == '2' else False
    print('---')       
    
    for root, dirs, files in os.walk(folder, topdown=False):

        for fname in files:
            if fname.endswith('.json') and not '_LRflipped' in fname:
                fname = os.path.join(root, fname)
                print(' - Processing ' + fname + '...', end=' ', flush=False)
                content = json.load(open(fname,'r'))
                
                if type(content) == list:

                    newcontent = []
                    for jdict in content:
                        if 'triplets' in jdict.keys():            # MeshView JSON
                            coords = jdict['triplets']
                            flipped = flip_json_anchors(coords)
                            jdict.update({'triplets':flipped})
                            newcontent.append(jdict)

                        else:
                            print('Unsupported JSON format')
                            break

                elif type(content) == dict:

                    newcontent = {}
                    if 'slices' in content.keys():                # QuickNII JSON
                        newslices = []
                        for s in content['slices']:
                            coords = s['anchoring']
                            flipped = flip_json_anchors(coords)
                            s.update({'anchoring':flipped})
                            newslices.append(s)
                        content.update({'slices':newslices})
                        newcontent = content

                    else:
                        print('Unsupported JSON format')
                        break
                                          
                else:
                    print('Unsupported JSON format')
                    continue

                json.dump(newcontent, open(fname[:-5] + '_LRflipped.json', 'w'), indent=4)
                print('Done.')

            elif fname.endswith('.xml') and not '_LRflipped' in fname:
                fname = os.path.join(root, fname)
                print(' - Processing ' + fname + '...', end=' ', flush=False)

                lines = []
                with open(fname, 'r') as xmlf:
                    for line in xmlf:
                        if line.strip().startswith('<slice filename='):
                            new = flip_xml_anchors(line)
                            lines.append(new)                
                        else:
                            lines.append(line)

                with open(fname[:-4] + '_LRflipped.xml', 'w') as outf:
                    for line in lines:
                        outf.write(line)

                print('Done.')
