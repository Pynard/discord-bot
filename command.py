
import re
import pickle
import base64
import asyncio
from datetime import datetime, timedelta

from config import *

def help_cmd(cmd):
    return f"{g_bot_token}{Command.__dict__[cmd].__doc__}"

async def update_flags():
    try:
        content = pickle.load(open('data/flags','rb'))
    except FileNotFoundError:
        return

    padding = max([ len(elt) for elt in content.keys() ])+1
    msg = '\n'.join([ '{:<{}} --> {}'.format(chall,padding,flag) for chall,flag in content.items() ])

    flag_chan = client.get_channel(g_channels['flags'])
    await flag_chan.purge()
    await flag_chan.send(f'```{msg}```')

async def update_timers():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            timers = pickle.load(open('data/timer','rb'))
        except FileNotFoundError:
            pass

        else:
            to_delete = []
            for name,(channel_id,msg_id,finish) in timers.items():
                remaining = finish-datetime.now()
                if remaining.total_seconds() <= 0:
                    to_delete += [name]
                    continue

                else:
                    text = str((finish-datetime.now())).split('.')[0]
                    text = ' **:** '.join([ ''.join([ g_big_numbers[digit] for digit in elt ]) for elt in text.split(':') ])

                    chan = client.get_channel(channel_id)
                    msg = await chan.fetch_message(msg_id)
                    await msg.edit(content=text)

            if to_delete:
                for name in to_delete:
                    channel_id,msg_id,_ = timers[name]
                    chan = client.get_channel(channel_id)
                    msg = await chan.fetch_message(msg_id)
                    await msg.edit(content="**FINI !!**")

                    del timers[name]
                    pickle.dump(timers,open('data/timer','wb'))

        await asyncio.sleep(1)


class Command:

    async def flag(message):
        'flag <flag>'
        cmd = re.search(f'{g_bot_token}(\S*)',message.content).group(1)

        flag_regex = re.search(f'{g_bot_token}flag\s+(.*)',message.content)

        error = ''
        if flag_regex is not None and len(flag_regex.groups()) == 1:
            if 'chall' in message.channel.name:
                flag = flag_regex.group(1)
                try:
                    content = pickle.load(open('data/flags','rb'))
                except FileNotFoundError:
                    content = {}
                content[message.channel.name.replace('chall_','')] = flag
                pickle.dump(content,open('data/flags','wb'))
                await update_flags()
                await message.channel.send(f"GG ! Enfin un qui ne fait pas partie de ceux qui ne sont rien")
                await message.channel.send(f"<{g_emoji['macron']}>") 

            else:
                error = f"блят ! Le channel **{message.channel.name}** n'est pas un channel associé a un challenge... <{g_emoji['stalin']}>"
        else:
            error = f"Essayes pas de m'enculer !\nC'est comme ça que ça marche :\n```{help_cmd(cmd)}```"

        if error:
            await message.channel.send(f'{message.author.mention} '+error)

    async def emoji(message):
        'emoji'
        msg = ' '.join([ f'<{elt}>' for elt in g_emoji.values() ])
        await message.channel.send(msg)

    async def b64(message):
        'b64 <enc/dec> <message>'
        cmd = re.search(f'{g_bot_token}(\S*)',message.content).group(1)
        error = ''

        msg_input = re.search(f'{g_bot_token}b64\s+(enc|dec)\s+(.*)',message.content)
        if msg_input:
            compute = base64.b64encode if msg_input.group(1) == 'enc' else base64.b64decode
            msg = compute(msg_input.group(2).encode()).decode()
            await message.channel.send(f'{message.author.mention} {msg}');
        else:
            error = f"L'encodage et le décodage en b64, C'est comme ça que ça marche :\n```{help_cmd(cmd)}```"
        if error:
            await message.channel.send(f'блят {message.author.mention} ! '+error)

    async def list_cmd(message):
        'list_cmd'
        msg = '__Voila la liste des commandes camarade !__\n```'
        msg += '\n'.join([ '{:<15} :     {}'.format(cmd,help_cmd(cmd)) for cmd in Command.__dict__.keys() if '__' not in cmd ])
        msg += '\n```'
        await message.channel.send(f'{message.author.mention} {msg}')

    async def timer(message):
        'timer "<name>" [#d] [#h] [#m] [#s]'
        cmd = re.search(f'{g_bot_token}(\S*)',message.content).group(1)
        error = ''

        parse_regex = re.search(f'{g_bot_token}timer\s+\"(.+)\"\s*(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?',message.content)
        if not parse_regex:
            await message.channel.send(f'блят {message.author.mention} ! Ptin lis la doc bordel... :\n```{help_cmd(cmd)}```'+error)
            return

        params = parse_regex.groups()
        name = params[0]
        time_params = params[1:]
        duration = sum([ int(elt[:-1])*g_time_convert[elt[-1]] for elt in time_params if elt])

        if not name:
            error = f"Donne un nom à ton timer...le pauvre...<{g_emoji['darmanin']}>"
        elif duration == 0:
            error = f"Pas de timer de moins de 0 seconde ! Et si vous pensez le contraire nous ne sommes pas dans le même camp madame !"
        if error:
            await message.channel.send(f'блят {message.author.mention} ! '+error)
            return
        
        finish = datetime.now()+timedelta(seconds=duration)
        msg = f'**{name}**'
        await message.channel.send(f'{msg}')
        msg_id = (await message.channel.send('...')).id

        try:
            timers = pickle.load(open('data/timer','rb'))
        except FileNotFoundError:
            timers = {}

        timers[name] = [message.channel.id,msg_id,finish] 
        pickle.dump(timers,open('data/timer','wb'))
        

        


