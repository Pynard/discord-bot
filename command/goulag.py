
import re
import pickle
import asyncio

from global_var import *
from .decorator import *

@error
async def cmd(message):
    'goulag add/free <username>'
    msg_input = re.search(f'{g_bot_token}goulag\s+(add|free)\s+(\S+)',message.content)

    if msg_input:
        option,username = msg_input.groups()


        # search for user on server
        member = client.guilds[0].get_member_named(username)
        if not member:
            return f"**{username}** n'a pas été trouvé sur le territoire de notre mère Russie"

        if option == 'add':
            if 'maxigir' in username and message.author.name != 'maxigir':
                await message.channel.send(f"Camarade **{message.author.mention}** vous êtes accusé de haute trahison, envers notre leader et notre mère Russie !")
                await message.channel.send(f"<{g_emoji['stalin']}>")
                member = message.author
            return await add(member)

        elif option == 'free':
            if 'maxigir' in username and message.author.name != 'maxigir':
                await message.channel.send(f"Votre tentative de libérer notre leader est apréciable, mais le fait de penser que notre père puisse être incarcéré est un manque cruel de foi envers notre leader et est vu comme une trahison aux yeux du parti")
                await message.channel.send(f"<{g_emoji['stalin']}>")
                member = message.author
                return await add(member)
            if message.author.name in username and message.author.name != 'maxigir':
                return "Personne ne peut échapper à un camp sibérien"
            return await free(member)
    else:
        return "Veuillez correctement remplir le formulaire de gestion du goulag camarade"

async def add(member):
    goulag_role = client.guilds[0].get_role(g_roles['goulag'])
    goulag_channel = client.get_channel(g_channels['goulag'])

    goulag_content = load_goulag_data()

    # Check if member already is in goulag
    if member.name in goulag_content.keys():
        return f"Le dissident **{member.name}** a déjà été envoyé au goulag !"

    # Generate zek id
    try:
        zek_id = max([ zek['id'] for zek in goulag_content.values() ]) + 1
    except ValueError:
        zek_id = 0

    # Write member in goulag data
    goulag_content[member.name] = { 'roles' : [ elt.id for elt in member.roles if '@' not in elt.name],
                                    'id' : zek_id }
    save_goulag_data(goulag_content)

    # Put member to goulag
    try:
        await member.remove_roles(*[elt for elt in member.roles if '@' not in elt.name])
        await member.add_roles(goulag_role)
        await member.move_to(goulag_channel)
        await member.edit(nick='заключённый - {:03d}'.format(zek_id))
    except:
        pass

async def free(member):
    goulag_role = client.guilds[0].get_role(g_roles['goulag'])
    goulag_channel = client.get_channel(g_channels['goulag'])

    goulag_content = load_goulag_data()

    for name,zek in goulag_content.items():
        if name == member.name:
            try:
                await member.remove_roles(goulag_role)
                await member.add_roles(*[ client.guilds[0].get_role(elt) for elt in zek['roles'] ])
                await member.move_to(client.get_channel(g_channels['voice']))
                await member.edit(nick=None)
            except:
                pass

            del goulag_content[name]
            save_goulag_data(goulag_content)
            return

    return f"Le camarade **{member.name}** n'a pas été trouvé au goulag...son cadavre sera retrouvé au printemps à la fonte des neiges"

def load_goulag_data():
    try:
        goulag_content = pickle.load(open(g_data_dir+'/goulag','rb'))
    except FileNotFoundError:
        goulag_content = {}
    return goulag_content

def save_goulag_data(content):
    pickle.dump(content,open(g_data_dir+'/goulag','wb'))

async def manage_goulag_music():
    await client.wait_until_ready()
    voice_client = await client.get_channel(g_channels['goulag']).connect()

    while not client.is_closed():
        goulag_content = load_goulag_data()

        if goulag_content and not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="local/goulag/soviet-anthem.mp3"))

        elif not goulag_content and voice_client.is_playing():
            voice_client.stop()

        await asyncio.sleep(1)
