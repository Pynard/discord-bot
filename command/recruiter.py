import random
import re

from .decorator import *
from global_var import *
from os import listdir
from os.path import isfile, join

def loadTemplateDb():
    dbPath =  g_local_dir+"/recruiter/templates"
    onlyfiles = [f for f in listdir(dbPath) if isfile(join(dbPath, f))]
    db=[]
    for f in onlyfiles:
        text_file = open(dbPath+"/"+f, "r")
        template = text_file.read()
        db.append(template);
        text_file.close();
    return db

def loadGrammarDb():
    dbPath =  g_local_dir+"/recruiter/grammar"
    onlyfiles = [f for f in listdir(dbPath) if isfile(join(dbPath, f))]
    db={}
    for f in onlyfiles:
        text_file = open(dbPath+"/"+f, "r")
        key_name = f.replace(".txt","");
        lines = text_file.readlines()
        lines=list(map(str.strip, lines))
        db = {**{ key_name: lines } , **db}
        text_file.close();
    return db

def bullshit_it(template):
    field_regex = re.search(f'\<(\w+)\#?\>',template)
    while field_regex is not None and len(field_regex.groups()) == 1:
        field_name =  field_regex.group(1)
        if(field_name == "br"):
            template=template.replace("<br>","\n")
        elif field_name == "name":
            template = template.replace("<name>","#name#")
        else:
            field_key=field_name.replace("#","")
            selected = random.choice(grammar[field_key])
            template = template.replace("<"+field_key+">",selected)
            template = template.replace("<"+field_key+"#>",selected)
        field_regex = re.search(f'\<(\w+)\#?\>',template)
    return template;


def recruting(name):
    template = random.choice(templateDb)
    pipo = bullshit_it(template).replace("#name#",name);
    return (pipo)

@error
async def cmd(message):
    'recruting'
    msg = recruting(message.author.mention)
    await message.channel.send(msg)

templateDb = loadTemplateDb()
grammar = loadGrammarDb()
