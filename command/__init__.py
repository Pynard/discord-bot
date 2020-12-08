
import re
import pickle
import base64

from global_var import *

from .decorator import *
from . import timer
from . import flag
from . import b64
from . import emoji
from . import pipo

class Command:

    @inplace
    @error
    async def list_cmd(message):
        'list_cmd'
        msg = '__Voila la liste des commandes camarade !__\n```'
        msg += '\n'.join([ '{:<15} :     {}'.format(cmd,func.__doc__) for cmd,func in Command.__dict__.items() if '__' not in cmd ])
        msg += '\n```'
        await message.channel.send(f'{message.author.mention} {msg}')

    @error
    async def flag(message):
        'flag <flag>'
        return await flag.cmd(message)

    @error
    async def emoji(message):
        'emoji'
        return await emoji.cmd(message)

    @inplace
    @error
    async def pipo(message):
        'pipo'
        return await pipo.cmd(message)

    @error
    async def b64(message):
        'b64 <enc/dec> <message>'
        return await b64.cmd(message)

    @inplace
    @error
    async def timer(message):
        'timer "<name>" [#d] [#h] [#m] [#s]'
        return await timer.cmd(message)
