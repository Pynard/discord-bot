
import re
import random

from global_var import *
from ..decorator import *
from .utils import *
from .gg import gg_dict

@error
@dev_only
async def cmd(message):
    'ctf create <nom> https://ctftime.org/event/<event>\nctf dump <nom>'

    pattern_url = 'https://ctftime\.org/event/\d+' 
    params = re.search(f'{g_bot_token}ctf\s+(create|dump)\s+(\S+)\s+({pattern_url})',message.content)

    if not params:
        return 'Tes paramètres sont chelous...'

    action = params.group(1)
    name = params.group(2).upper()
    url = params.group(3)

    if action == 'create':
        ctf_data, error = await create_category(name)
        if not ctf_data:
            return error

        ctf_data['challenge'] = {}
        await write_info(ctf_data['infos'], url,ctf_data)
        save_ctf(name,ctf_data)

@error
async def add_challenge(message):
    'chall <nom>'
    
    if not is_ctf(message.channel):
        return 'C\'est ptetre un peu dur a comprendre mais faut se trouver dans un ctf pour add un challenge'

    param = re.search('&chall\s(\S+)',message.content)
    if not param:
        return 'Faut lui donner un nom à ton challenge...ça semble évident...mais pas pour tout le monde visiblement'

    ctf_data = load_ctf(message.channel.category)

    name = param.group(1)
    guild = client.guilds[0]
    category = client.get_channel(ctf_data['category'])
    ctf_data['challenge'][name] = { 'id': (await guild.create_text_channel(name,category=category)).id, 'flag':None }

    save_ctf(category.name,ctf_data)

@error
async def flag(message):
    'flag <flag>'
    param = re.search(f'{g_bot_token}flag\s+(.*)',message.content)

    if not param: 
        return "Essayes pas de m'enculer ! C'est comme ça que ça marche"

    if not is_ctf(message.channel):
        return 'Merci de rentrer les flags dans les CTF, mais c\'est ptetre trop te demander...?'

    ctf_name = message.channel.category
    ctf_data = load_ctf(ctf_name)

    if message.channel.name not in ctf_data['challenge'].keys():
        return f"Le channel **{message.channel.name}** n'est pas un channel associé a un challenge... <{g_emoji['stalin']}>"

    flag = param.group(1)
    ctf_data['challenge'][message.channel.name]['flag'] = flag
    save_ctf(ctf_name,ctf_data)

    
    gg_msg = random.choice(gg_dict)
    for elt in gg_msg:
        await message.channel.send(elt)

    await update_flags(ctf_data)

