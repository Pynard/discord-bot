
import re
from config import *

devs = ['maxigir','lsorignet']

def is_dev(name):
    return True if name in devs else False

async def add_flag(message):
    flag_regex = re.search(f'{bot_token}flag\s*=\s*(.*)',message.content)

    if flag_regex is not None and len(flag_regex.groups()) == 1:
        flag = flag_regex.group(1)
        print(flag)

    else:
        error = f"Essaye pas de m'enculer !\nC'est comme ça que ça marche : ```{bot_token}flag = <flag>```"
        await message.channel.send(f'{message.author.mention} '+error)

async def test_emoji(message):
    if is_dev(message.author.name):
        msg = '\n'.join([ f'<{elt}>' for elt in emoji.values() ])
        await message.channel.send(msg)
