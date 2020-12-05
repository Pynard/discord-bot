# bot.py
import os
import re

import discord
from dotenv import load_dotenv

from config import *
from command import * 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"{member.mention} Heil {member.name} ! Willkommen im reich <{emoji['hitler']}>")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.match(f'{bot_token}flag',message.content):
        await add_flag(message)
    elif re.match(f'{bot_token}test_emoji',message.content):
        await test_emoji(message)

client.run(TOKEN)


#if 'lsorignet' in str(message.author.name):
#    await message.channel.send(f"lsorignet n'a pas le droit d'utiliser cette commande <{emoji['hitler']}>")
#    return

