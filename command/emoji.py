
from global_var import *
from .decorator import *

@error
async def cmd(message):
    'emoji'
    msg = ' '.join([ f'<{elt}>' for elt in g_emoji.values() ])
    await message.channel.send(msg)
