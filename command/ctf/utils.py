import re
import requests
import pickle
from bs4 import BeautifulSoup

from global_var import *

def parse_url(url):
    html_text = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(html_text, 'html.parser')

    for br in soup.findAll('br'):
        br.replace_with('\n')

    # try 1
    infos = soup.find(name='div', attrs={'class':'span10'}).text
    date = re.search('((Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s(\d*)\s(Jan|Fev|Mar|Apr|May|Jun|Jui|Aug|Sep|Oct|Nov|Dec)\.\s(\d+),\s(\d+):(\d+)\sUTC.*UTC)',infos).group(1)
    title = re.search('An?\s(.*)\.',infos).group(1)
    ctf_format = re.search('(Format:.*\xa0)',infos).group(1)
    ctf_url = re.search('Official URL:\s+(.*/)',infos).group(1)

    try:
        description = soup.find(name='div', attrs={'class':'well','id':'id_description'}).find('p').text
        description = '\n'.join([elt.text for elt in soup.find(name='div', attrs={'class':'well','id':'id_description'}).findAll('p')]) 
    except:
        description = None

    try:
        prizes = '\n'.join([ elt.text for elt in soup.find(name='div', attrs={'class':'well','id':''}).findAll('p') ])
    except:
        prizes = None
    
    try:
        icon = '/'.join(url.split('/')[:-2]) + soup.find(name='div', attrs={'class':'span2'}).find('img').get('src')
    except:
        icon = None

    embed = discord.Embed(title=title.upper(), url=ctf_url, description=':calendar: **'+date+'**', color=0xffa200)
    if icon:
        embed.set_thumbnail(url=icon)
    if description:
        embed.add_field(name=':page_facing_up: Description', value='```'+description+'```', inline=False)
    if prizes:
        embed.add_field(name=':trophy: Prizes', value='```'+prizes+'```', inline=False)

    # /!\ # IN CASE OF EMERGENCY BRAKE THE COMMENTS /!\
    # /!\ #
    # /!\ # poor man lazy method...
    # /!\ #
    # /!\ # out = "```"+soup.find(name='div', attrs={'class':'span10'}).text+"```"
    # /!\ # icon = '/'.join(url.split('/')[:-2]) + soup.find(name='div', attrs={'class':'span2'}).find('img').get('src')
    
    return embed

async def write_info(channel_id,url,ctf_data):
    channel = client.get_channel(channel_id)
    ctf_desc = parse_url(url)

    ctf_desc.add_field(name=':triangular_flag_on_post: Flags', value="No first blood yet !", inline=False)
    ctf_data['flags'] = { 'id': (await channel.send(embed=ctf_desc)).id, 'embed': ctf_desc }

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

