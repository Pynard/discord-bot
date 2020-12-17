
import re
import base64
import os

from global_var import *

from .utils import *
from .decorator import *





def get_category_from_name(guild, name):
    for category in guild.categories:
        if category.name.upper() == name.upper():
            return category
    return None

async def dump_chall(channel,path):
    chall_name = channel.name
    flag = "not found"
    #checking if old format
    if chall_name.startswith('chall_'):
        chall_name = chall_name[6:];
    dump_path = path+"/challenges/"+chall_name+".md"
    dump_ressource_path = "../attachements/"+chall_name

    f = open(dump_path, "w")
    f.write("# "+chall_name.upper()+"\n")
    async for m in channel.history(limit=500, oldest_first=True):
        content = m.content
        if content.startswith(g_bot_token+"flag "):
            content = content[6:]
            flag = content
            content = "flag : `"+content+"`"
        f.write(content+"\n")
        for e in m.embeds:
            print(e.type)
            if(e.type == "image"):
                f.write("![image]("+e.url+" \"image\")\n")
            elif e.type == "link":
                f.write("["+e.title+"]("+e.url+")\n")
        for a in m.attachments:
            chall_attachment_path = path+"/attachements/"+chall_name
            mkPath(chall_attachment_path)
            download(a.url,chall_attachment_path+"/"+a.filename)
            if a.filename.endswith(".png") or a.filename.endswith(".jpg") or a.filename.endswith(".gif"):
                f.write("!["+a.filename+"]("+dump_ressource_path+"/"+a.filename+" \""+a.filename+"\")\n")
            else:
                f.write("- Fichier : ["+a.filename+"]("+dump_ressource_path+"/"+a.filename+")\n")
    f.close()
    return flag

def add_summary_to_index(dict,path):

    f = open(path, "a")
    f.write("\n##  WRITE UPS\n\n| Name | Flags |\n| ------------- | :----:|\n")
    for key, value in dict.items():
        #if old keys
        if key.startswith('chall_'):
            key = key[6:];
        f.write("|["+key+"](challenges/"+key+".md)|`"+value+"`| \n")
    f.close()

@error
async def cmd(message):
    'dump <ctf>'
    msg_input = re.search(f'{g_bot_token}dump\s+(.*)',message.content)
    if msg_input:
        ctf =  msg_input.group(1)
        ctf_cat = get_category_from_name(message.guild, ctf)
        dic = {}
        if ctf_cat != None:
            path = g_dump_dir+"/"+ctf_cat.name.upper()
            mkPath(path+"/challenges")
            for channel in ctf_cat.channels:
                if(channel.name != "général" and channel.name != "flags"):
                    if channel.name == "infos":
                       await dump_chall(channel, path)
                    else:
                        dic[channel.name] = await dump_chall(channel, path)

            os.replace(path+"/challenges/infos.md", path+"/README.md")
            add_summary_to_index(dic,path+"/README.md")
        msg = "dump ok !"
        await message.channel.send(f'{message.author.mention} {msg}');
    else:
        return "Le dumping d'un évenement CTF, C'est comme ça que ça marche"
