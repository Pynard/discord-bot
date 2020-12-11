
import re
import pickle

from global_var import *
from .decorator import *

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

@error
async def cmd(message):
    'flag <flag>'
    flag_regex = re.search(f'{g_bot_token}flag\s+(.*)',message.content)

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
            return f"Le channel **{message.channel.name}** n'est pas un channel associé a un challenge... <{g_emoji['stalin']}>"
    else:
        return "Essayes pas de m'enculer ! C'est comme ça que ça marche"

