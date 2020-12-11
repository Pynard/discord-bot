
import re
import pickle
import asyncio
from datetime import datetime, timedelta

from global_var import *
from .decorator import *

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


@error
async def cmd(message):
    'timer "<name>" [#d] [#h] [#m] [#s]'
    cmd = re.search(f'{g_bot_token}(\S*)',message.content).group(1)
    error = ''

    parse_regex = re.search(f'{g_bot_token}timer\s+\"(.+)\"\s*(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?',message.content)
    if not parse_regex:
        return 'Ptin lis la doc bordel...'

    params = parse_regex.groups()
    name = params[0]
    time_params = params[1:]
    duration = sum([ int(elt[:-1])*g_time_convert[elt[-1]] for elt in time_params if elt])

    if not name:
        return f"Donne un nom à ton timer...le pauvre...<{g_emoji['darmanin']}>"
    elif duration == 0:
        return f"Pas de timer de moins de 0 seconde ! Et si vous pensez le contraire nous ne sommes pas dans le même camp madame !"

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
