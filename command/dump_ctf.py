
import re
import base64

from global_var import *
from .decorator import *


@error
async def cmd(message):
    'dump <ctf>'
    msg_input = re.search(f'{g_bot_token}dump\s+(.*)',message.content)
    if msg_input:
        ctf =  msg_input.group(1)
        msg = "dump ok !"
        await message.channel.send(f'{message.author.mention} {msg}');
    else:
        return "Le dumping d'un évenement CTF, C'est comme ça que ça marche"
