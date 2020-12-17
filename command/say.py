
import re

from global_var import *
from .decorator import *

@error
@dev_only
async def cmd(message):
    'say <channel_id> <message>'
    params = re.search(f'{g_bot_token}say\s(\d+)\s(.*)',message.content)

    if not params:
        return 'La doc !! c\'est pas compliqué pourtant'

    channel_id, msg = params.groups()
    channel = client.get_channel(int(channel_id))
    await channel.send(msg)
