import os
import xml.etree.ElementTree as ET
import argparse

#from matplotlib import pyplot as plt

SIMULATE = False


def file_rename(path, org, dest):
    global SIMULATE

    #Verifica que existe el origen y no existe el destino
    porg = os.path.join(path,org)
    pdest = os.path.join(path, dest)

    #Si origen = destino, ya estaba renombrado
    if porg == pdest:
        return True

    if os.path.exists(porg) and not os.path.exists(pdest):
        if not SIMULATE:
            os.rename(porg, pdest)
        return True
    else:
        return False


def process_audioclips_rename(path, name, db):
    global SIMULATE

    audio_id = 0
    song_name = os.path.splitext(name)[0]

    tree = ET.parse(os.path.join(path, name))
    root = tree.getroot()

    print("  firmware: %s" % root.attrib['firmwareVersion'])

    for section in root:
        if section.tag == "sessionClips" or section.tag == "arrangementOnlyTracks":
            for clip in section:
                #Encontradado un clip de audio no vacio
                if clip.tag == "audioClip" and len(clip.attrib["filePath"])>0:
                    
                    audioclip_path = clip.attrib["filePath"]
                    print("  - Find audioclip ", audioclip_path)

                    if audioclip_path not in db.keys():
                        audio_id += 1
                        rel_path = os.path.split(audioclip_path)[0]
                        
                        #Genero el nuevo nombre
                        dest_name = song_name.replace(' ', '_')
                        dest = os.path.join(
                            rel_path, dest_name + "_%02d.WAV" % audio_id)
                        #Muevo el fichero
                        rename_status = file_rename(os.path.join(
                            path, ".."), audioclip_path, dest)

                        if rename_status:
                            print("    Moved file %s to %s" % (audioclip_path, dest))
                            db[audioclip_path] = dest
                            clip.attrib["filePath"] = dest
                            if not SIMULATE:
                                tree.write(os.path.join(path, name))
                            print("    Relinked clip to %s" % dest)
                        else:
                            print("    !Problems renaming file, not changes has been made.")  
                    else:
                        dest = db[audioclip_path]
                        clip.attrib["filePath"] = dest
                        if not SIMULATE:
                            tree.write(os.path.join(path, name))
                        print("    Relinked clip to %s" % dest)


def process_instruments(path, name, db):

    audio_id = 0
    song_name = os.path.splitext(name)[0]

    tree = ET.parse(os.path.join(path, name))
    root = tree.getroot()

    used_instruments = []
    for section in root:
        if section.tag == "instruments":
            for instrument in section:
                #Encontradado un clip de audio no vacio
                if instrument.tag == "sound":
                    if "presetName" in instrument.attrib.keys():
                        preset = instrument.attrib["presetName"]
                    else:
                        preset = instrument.attrib["presetSlot"]
                    used_instruments.append(preset)
                    if preset in db.keys():
                        db[preset]+=1
                    else:
                        db[preset]=0

    print("  Used instruments: %s" % used_instruments)

    return used_instruments


if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Simple Deluge Helper for Clips Organization"
    )   

    parser.add_argument('path', help="Path of Deluge Song folder")
    parser.add_argument('-s', help="Simulate changes with no HD changes",
        action="store_true")   
    parser.add_argument('-i', help="Show instrument stats of your songs",
        action="store_true")  

    args = parser.parse_args()

    path = args.path
    SIMULATE = args.s
    show_instruments = args.i

    if SIMULATE:
        print("Using simulate MODE, no changes will be made.")

    clipDB = {}
    instrumentDB = {}

    for s in sorted(os.listdir(path)):
        name = s.lower()
        if not name.startswith(".") and name.endswith(".xml"):
            # Para cada canción
            print("> Processing song '%s'" % s)
            process_audioclips_rename(path, s, clipDB)
            if show_instruments:
                process_instruments(path, s, instrumentDB)
            print("")

    print(instrumentDB)
    #plt.bar(instrumentDB.keys(), instrumentDB.values(), color='g')
    #plt.show()

