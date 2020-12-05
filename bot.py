# bot.py
import os

import discord
from dotenv import load_dotenv

import re

bot_token = '&'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

emoji = {   'hitler' : ':hitler:784774352838983691' }

async def add_flag(message):
    flag_regex = re.search(f'{bot_token}flag\s*=\s*(.*)',message.content)

    if flag_regex is not None and len(flag_regex.groups()) == 1:
        flag = flag_regex.group(1)
        print(flag)

    else:
        error = f"Essaye pas de m'enculer !\nC'est comme ça que ça marche : ```{bot_token}flag = <flag>```"
        await message.channel.send(f'{message.author.mention} '+error)


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

client.run(TOKEN)


#if 'lsorignet' in str(message.author.name):
#    await message.channel.send(f"lsorignet n'a pas le droit d'utiliser cette commande <{emoji['hitler']}>")
#    return

