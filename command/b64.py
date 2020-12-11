
import re
import base64

from global_var import *
from .decorator import *

@error
async def cmd(message):
    'b64 <enc/dec> <message>'
    msg_input = re.search(f'{g_bot_token}b64\s+(enc|dec)\s+(.*)',message.content)
    if msg_input:
        compute = base64.b64encode if msg_input.group(1) == 'enc' else base64.b64decode
        msg = compute(msg_input.group(2).encode()).decode()
        await message.channel.send(f'{message.author.mention} {msg}');
    else:
        return "L'encodage et le décodage en b64, C'est comme ça que ça marche"
