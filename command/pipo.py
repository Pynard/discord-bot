import random

from .decorator import *
from global_var import *
from os import listdir
from os.path import isfile, join


def loadPipoDb(name):
    dbPath = g_local_dir+"/dico_pipo/"+name
    onlyfiles = [f for f in listdir(dbPath) if isfile(join(dbPath, f))]
    onlyfiles.sort()
    db=[]
    for f in onlyfiles:
        text_file = open(dbPath+"/"+f, "r")
        lines = text_file.readlines()
        lines=list(map(str.strip, lines))
        db.append(lines);
        text_file.close();
    return db

def harmonize(pipo):
    harmonic = 'aeiouyhéèà'
    while pipo.find("#") != -1:
        idx = pipo.find("#");
        if idx+2 < len(pipo):
            char = pipo[idx+2]
            pipobegin = pipo[:idx]
            pipoend   = pipo[idx+1:]
            if char in harmonic:
                pipo = pipobegin + "'" +pipoend
            else :
                pipo = pipobegin + "e" +pipoend
    return pipo.strip()

def play_pipo():
    pipo = ""
    print(currentPipoDb)
    for pipodb in currentPipoDb:
        pipo=pipo+" "+random.choice(pipodb)
    pipo = harmonize(pipo)
    return (pipo)

@error
async def cmd(message):
    'pipo'
    msg = play_pipo()
    await message.channel.send(msg)


#Init dictionnary
currentPipoDb = loadPipoDb("manager")