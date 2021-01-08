
import re
import pickle
import base64

from global_var import *

from . import ctf
from . import timer
from . import b64
from . import emoji
from . import pipo
from . import recruiter
from . import say

class Command:

    async def cmd(message):
        'Liste les commandes\ncmd'
        embed = discord.Embed(title='__Voila la liste des commandes camarade !__')
        for cmd,func in Command.__dict__.items():
            if '__' not in cmd:
                desc = func.__doc__.split('\n')[0]
                usage = f'```{g_bot_token}'+f'\n{g_bot_token}'.join(func.__doc__.split('\n')[1:])+'```'
                embed.add_field(name=cmd, value=f'*{desc}*\n{usage}', inline=False)
        await message.channel.send(embed=embed)

    async def ctf(message):
        'Gère les ctf\nctf create nom https://ctftime.org/event/<event>\nctf dump <nom>'
        return await ctf.cmd(message)

    async def chall(message):
        'Crée un nouveau challenge\nchall <nom>'
        return await ctf.add_challenge(message)

    async def flag(message):
        'Enregistre un flag\nflag <flag>'
        return await ctf.flag(message)

    async def emoji(message):
        'Liste les emojis du serveur\nemoji'
        return await emoji.cmd(message)

    async def pipo(message):
        'Génère un discours managérial\npipo'
        return await pipo.cmd(message)

    async def recruiting(message):
        'Faites vous recruter\nrecruiting'
        return await recruiter.cmd(message)

    async def b64(message):
        'Encode/Decode en base64\nb64 <enc/dec> <message>'
        return await b64.cmd(message)

    async def timer(message):
        'Crée un countdown\ntimer "<name>" [#d] [#h] [#m] [#s]'
        return await timer.cmd(message)

    async def say(message):
        'Envoie un message en tant que bot\nsay <channel_id> <message>'
        return await say.cmd(message)
