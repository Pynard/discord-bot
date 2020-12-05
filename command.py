
import re
import base64

from config import *

def is_dev(name):
    return True if name in devs else False

def help_cmd(cmd):
    return f"{bot_token}{Command.__dict__[cmd].__doc__}"

def read_flag():
    with open('data/flags.txt','r') as f:
        return { chall : flag for chall,flag in [ line.split(';') for line in f.read().splitlines() ] }

def write_flag(content):
    with open('data/flags.txt','w') as f:
        f.write('\n'.join([ f'{chall};{flag}' for chall,flag in content.items() ]))

async def refresh_flags():
    flag_chan = client.get_channel(channels['flags'])
    await flag_chan.purge()
    msg = '\n'.join([ '{:<20} --> {}'.format(*item) for item in read_flag().items() ])
    await flag_chan.send(f'```{msg}```')

class Command:

    async def flag(message):
        'flag = <flag>'
        cmd = re.search(f'{bot_token}(\S*)',message.content).group(1)
        flag_regex = re.search(f'{bot_token}flag\s*=\s*(.*)',message.content)

        error = ''
        if flag_regex is not None and len(flag_regex.groups()) == 1:
            if 'chall' in message.channel.name:
                flag = flag_regex.group(1)
                content = read_flag()
                content[message.channel.name] = flag
                write_flag(content)
                await refresh_flags()

            else:
                error = f"блят ! Le channel **{message.channel.name}** n'est pas un channel associé a un challenge... <{emoji['stalin']}>"
        else:
            error = f"Essayes pas de m'enculer !\nC'est comme ça que ça marche :\n```{help_cmd(cmd)}```"

        if error:
            await message.channel.send(f'{message.author.mention} '+error)

    async def test_emoji(message):
        'test_emoji'
        msg = ' '.join([ f'<{elt}>' for elt in emoji.values() ])
        await message.channel.send(msg)

    async def enc_b64(message):
        'enc_b64 = <message>'
        msg_toenc = re.search(f'{bot_token}enc_b64\s*=\s*(.*)',message.content)
        if len(msg_toenc.groups()) == 1:
            msg = base64.b64encode(msg_toenc.group(1))
            await message.channel.send(msg);
        else:
            error = f"L'encodage en b64, C'est comme ça que ça marche :\n```{help_cmd(enc_b64.__name__)}```"
        if error:
            await message.channel.send(f'блят {message.author.mention} ! '+error)

    async def dec_b64(message):
        'dec_b64 = <message>'
        msg_toenc = re.search(f'{bot_token}dec_b64\s*=\s*(.*)',message.content)
        if len(msg_toenc.groups()) == 1:
            msg = base64.b64encode(msg_toenc.group(1))
            await message.channel.send(msg);
        else:
            error = f"Le décodage en b64, C'est comme ça que ça marche :\n```{help_cmd(dec_b64.__name__)}```"
        if error:
            await message.channel.send(f'блят {message.author.mention} ! '+error)

    async def list_cmd(message):
        'list_cmd'
        msg = '__Voila la liste des commandes camarade !__\n```'
        msg += '\n'.join([ '{:<15} :     {}'.format(cmd,help_cmd(cmd)) for cmd in Command.__dict__.keys() if '__' not in cmd ])
        msg += '\n```'
        await message.channel.send(f'{message.author.mention} {msg}')


