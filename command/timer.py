
import re
import pickle
import asyncio
from datetime import datetime, timedelta

from global_var import *
from .decorator import *

def timer_text(duration,hms=3):
    total_sec = duration.total_seconds()
    day,_ = divmod(total_sec,g_time_convert['d'])
    time = str(duration)
    if day != 0:
        time = time.split(', ')[-1]
    time = time.split('.')[0]

    text = ''
    if day != 0:
        text += ''.join([ g_big_numbers[digit] for digit in str(int(day)) ]) + ''.join([f':regional_indicator_{elt}:' for elt in 'day'])
        if day > 1:
            text += ':regional_indicator_s:'
        text += ' '*5
    text += (':regional_indicator_{}:     '.join(
        [ ''.join([ g_big_numbers['0']*(2-len(elt))+g_big_numbers[digit] for digit in elt ]) for i,elt in enumerate(time.split(':')) if i < hms ])
        +':regional_indicator_{}:').format(*'hms')

    return text

async def update_timers():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            timers = pickle.load(open(g_data_dir+'/timer','rb'))
        except FileNotFoundError:
            pass

        else:
            to_delete = []
            for timer_id,timer in timers.items():
                remaining = timer['finish']-datetime.now()
                if remaining.total_seconds() <= 0:
                    to_delete += [timer_id]
                    continue

                else:
                    text = timer_text(timer['finish']-datetime.now())
                    chan = client.get_channel(timer['channel_id'])
                    msg = await chan.fetch_message(timer['msg_id'])
                    await msg.edit(content=text)

            if to_delete:
                for timer_id in to_delete:
                    chan = client.get_channel(timers[timer_id]['channel_id'])
                    msg = await chan.fetch_message(timers[timer_id]['msg_id'])
                    await msg.edit(content="**FINI !!**")

                    del timers[timer_id]
                    pickle.dump(timers,open(g_data_dir+'/timer','wb'))

        await asyncio.sleep(1)

async def write_timer(channel,name,duration):
    finish = datetime.now()+duration
    header_id = (await channel.send(f'{name}')).id
    msg_id = (await channel.send('...')).id

    try:
        timers = pickle.load(open(g_data_dir+'/timer','rb'))
    except FileNotFoundError:
        timers = {}

    timer_id = len(timers)
    current_timer = {'name': name, 'channel_id': channel.id, 'msg_id':msg_id, 'finish': finish }
    timers[timer_id] = current_timer
    pickle.dump(timers,open(g_data_dir+'/timer','wb'))

    return header_id, msg_id

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
    duration = timedelta(seconds=sum([ int(elt[:-1])*g_time_convert[elt[-1]] for elt in time_params if elt]))

    if not name:
        return f"Donne un nom à ton timer...le pauvre...<{g_emoji['darmanin']}>"
    elif duration == 0:
        return f"Pas de timer de moins de 0 seconde ! Et si vous pensez le contraire nous ne sommes pas dans le même camp madame !"

    await write_timer(message.channel,name,duration)
