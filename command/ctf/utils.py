import re
import requests
import pickle
import json
import asyncio
from os import listdir
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from global_var import *

from ..timer import write_timer

async def update_timers():
    await client.wait_until_ready()
    while not client.is_closed():
        for f in listdir(f'{g_data_dir}/ctf'):
            if f[0] != '.':
                ctf_data = load_ctf(f)

                msg_header,msg_content = ctf_data['timer']
                if msg_header and msg_content:
                    infos_channel = client.get_channel(ctf_data['infos'])
                    msg_header = await infos_channel.fetch_message(msg_header)
                    msg_content = await infos_channel.fetch_message(msg_content)

                    start = ctf_data['start']
                    finish = ctf_data['finish']
                
                    is_started = True if (start-datetime.now()).total_seconds() < -10 else False
                    is_finished = True if (finish-datetime.now()).total_seconds() < -10 else False

                    if is_started and not is_finished and 'commence' in msg_header.content:
                        await msg_header.delete()
                        await msg_content.delete()
                        ctf_data['timer'] = await write_timer(infos_channel,'**Le CTF fini dans**',finish-datetime.now())
                        save_ctf(f,ctf_data)
                    elif is_finished:
                        await msg_content.delete()
                        await msg_header.edit(content='**Le CTF est fini !**')
                        ctf_data['timer'] = [None]*2 
                        save_ctf(f,ctf_data)
            
        await asyncio.sleep(10)
    
def parse_url(url):

    # get prizes by paring HTML page
    html_text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(html_text, 'html.parser')
    try:
        prizes = '\n'.join([ elt.text for elt in soup.find(name='div', attrs={'class':'well','id':''}).findAll('p') ])
    except:
        prizes = None


    # Get other informations with API
    event = re.search('.*\/(\d+)',url).group(1)
    url = f'https://ctftime.org/api/v1/events/{event}/'

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    event_dict = json.loads(response)

    parse_date = lambda date: date.split('T')[0]+' '+date.split('T')[1].split('+')[0].split(':')[0] + 'h UTC'
    start = parse_date(event_dict['start'])
    finish = parse_date(event_dict['finish'])
    duration = ''
    duration += str(event_dict['duration']['days']) + 'd ' if event_dict['duration']['days'] != 0 else ''
    duration += str(event_dict['duration']['hours']) + 'h '
    title = event_dict['title']
    ctf_format = event_dict['format']
    ctf_url = event_dict['url']
    description = event_dict['description']
    icon = event_dict['logo']

    start_dt = datetime.strptime(event_dict['start'].split('+')[0],'%Y-%m-%dT%H:%M:%S')+timedelta(hours=1)      # UTC+1
    finish_dt = datetime.strptime(event_dict['finish'].split('+')[0],'%Y-%m-%dT%H:%M:%S')+timedelta(hours=1)

    # create embed
    embed = discord.Embed(title=title.upper(), url=ctf_url, color=0xffa200)
    if icon:
        embed.set_thumbnail(url=icon)
    if ctf_format:
        embed.add_field(name='Format', value=ctf_format, inline=False)
    if start:
        embed.add_field(name='Start', value=start, inline=True)
    if start:
        embed.add_field(name='Finish', value=finish, inline=True)
    if duration:
        embed.add_field(name='duration', value=duration, inline=True)
    if description:
        embed.add_field(name=':page_facing_up: Description', value='```'+description+'```', inline=False)
    if prizes:
        embed.add_field(name=':trophy: Prizes', value='```'+prizes+'```', inline=False)

    return embed,start_dt,finish_dt
    #return embed,datetime.now()+timedelta(minutes=1),datetime.now()+timedelta(minutes=2)

async def write_info(channel_id,url,ctf_data):
    channel = client.get_channel(channel_id)
    ctf_desc,start_dt,finish_dt = parse_url(url)

    ctf_data['start'] = start_dt
    ctf_data['finish'] = finish_dt

    ctf_desc.add_field(name=':triangular_flag_on_post: Flags', value="```No first blood yet !```", inline=False)
    ctf_data['flags'] = { 'id': (await channel.send(embed=ctf_desc)).id, 'embed': ctf_desc }
    ctf_data['timer'] = await write_timer(channel,'**Le CTF commence dans**',start_dt-datetime.now())

def category_exists(name):
    guild = client.guilds[0]
    for category in guild.categories:
        if name == category.name:
            return True
    return False

async def create_category(name):
    if category_exists(name):
        return None,f'Alzheimer te guette, le CTF **{name}** existe déjà'

    ctf_data = {}
    guild = client.guilds[0]

    perms = { guild.default_role: discord.PermissionOverwrite(manage_channels=False) }
    category = await guild.create_category(name,overwrites=perms)
    ctf_data['category'] = category.id 
    await category.edit(position=0)

    perms = { guild.default_role: discord.PermissionOverwrite(send_messages=False) }
    ctf_data['infos'] = (await guild.create_text_channel('infos',category=category,overwrites=perms)).id
    ctf_data['general'] = (await guild.create_text_channel('général',category=category)).id

    return ctf_data, None

def is_ctf(channel):
    msg_category = channel.category
    if msg_category:
        try:
            ctf_data = load_ctf(msg_category)
        except FileNotFoundError:
            return False
    else:
        return False

    return True


def load_ctf(name):
    return pickle.load(open(g_data_dir+f'/ctf/{name}','rb'))

def save_ctf(name,content):
    pickle.dump(content,open(g_data_dir+f'/ctf/{name}','wb'))
    
async def update_flags(ctf_data):
    padding = max([ len(elt) for elt in ctf_data['challenge'].keys() ])+1
    msg = '\n'.join([ '{:<{}} --> {}'.format(challenge_name,padding,data['flag']) for challenge_name,data in ctf_data['challenge'].items() ])

    embed = ctf_data['flags']['embed'] 
    embed.remove_field(len(embed.fields)-1)
    embed.add_field(name=':triangular_flag_on_post: Flags', value='```'+msg+'```', inline=False)

    flag_msg = await (client.get_channel(ctf_data['infos'])).fetch_message(ctf_data['flags']['id'])
    await flag_msg.edit(embed=embed)

