
import re
import base64
import os

from global_var import *
from .decorator import *


def get_category_from_name(guild, name):
    for category in guild.categories:
        if category.name.upper() == name.upper():
            return category
    return None

@error
async def cmd(message):
    'dump <ctf>'
    msg_input = re.search(f'{g_bot_token}dump\s+(.*)',message.content)
    if msg_input:
        ctf =  msg_input.group(1)
        ctf_cat = get_category_from_name(message.guild, ctf)
        if ctf_cat != None:
            path = g_dump_dir+"/"+ctf_cat.name.upper()
            if not os.path.exists(path):
                os.makedirs(path)
            for channel in ctf_cat.channels:
                if(channel.name != "général"):
                    path = g_dump_dir+"/"+ctf_cat.name.upper()+"/"+channel.name.upper()+".md"
                    f = open(path, "w")
                    f.write("# "+channel.name.upper()+"\n")
                    async for m in channel.history(limit=500, oldest_first=True):
                        f.write (m.content+"\n")
                        for e in m.embeds:
                            print(e.to_dict())
                            if(e.type == "image"):
                                f.write("![image]("+e.url+" \"image\")\n")
                            elif e.type == "link":
                                f.write("["+e.title+"]("+e.url+")\n")
                    f.close()

        msg = "dump ok !"
        await message.channel.send(f'{message.author.mention} {msg}');
    else:
        return "Le dumping d'un évenement CTF, C'est comme ça que ça marche"
