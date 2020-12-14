import re
import os
from global_var import *
from command import Command
from command.timer import update_timers


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(update_timers())


@client.event
async def on_member_join(member):
    general = client.get_channel(g_channels['general'])
    await general.send(f"{member.mention} Heil {member.name} ! Willkommen im reich <{g_emoji['hitler']}>")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content or message.content[0] != g_bot_token:
        return
    if message.content == g_bot_token:
        await Command.list_cmd(message)
        return

    commands = [ elt for elt in Command.__dict__.keys() if '__' not in elt ]
    for cmd in commands:
        if re.match(f'{g_bot_token}{cmd}',message.content):
            await Command.__dict__[cmd](message)
            return


client.run(TOKEN)

