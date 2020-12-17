
import re
import pickle
import requests
import json
import asyncio
from bs4 import BeautifulSoup

from global_var import *

async def update_team_info():
    await client.wait_until_ready()

    day = 3600*24
    url = 'https://ctftime.org/api/v1/teams/141504/'
    while not client.is_closed():
        ### TEAM STATS

        # world total
        html_text = requests.get('https://ctftime.org/stats/', headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(html_text,'html.parser')
        world_total = soup.find(text=re.compile(r'\d+\steams\stotal'))
        world_total = world_total.split(' ')[0] 

        # country total
        country_total = soup.find(text=re.compile(r'FR'))
        country_total = re.search('(\d+)',country_total).group(1)

        # country rank
        html_text = requests.get('https://ctftime.org/team/141504', headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(html_text,'html.parser')
        country_rank = soup.find('a',attrs={ 'href': '/stats/FR' }).text

        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        team_dict = json.loads(response)
       
        infos_channel = client.get_channel(g_channels['infos'])

        rating = team_dict['rating'][0][list(team_dict['rating'][0].keys())[0]]

        embed = discord.Embed(title='Pynard', color=0xffa200)
        embed.set_image(url='https://cdn.discordapp.com/attachments/786896843308400641/786959340719439913/pynard.png')
        world = f"{rating['rating_place']}/{world_total}"
        country = f'{country_rank}/{country_total}'
        rating_points = '{:.2f}'.format(rating['rating_points'])

        embed.add_field(name='** **', value='** **', inline=False)
        embed.add_field(name=':earth_africa: Rank', value=world, inline=True)
        embed.add_field(name=':flag_fr: Rank', value=country, inline=True)
        embed.add_field(name=':game_die: Points', value=rating_points, inline=True)

        # remove embed
        await infos_channel.purge()

        # send embed
        await infos_channel.send(embed=embed)

        ### WRITEUPS
        embed=discord.Embed(title="Pynard Writeups", url="https://github.com/Pynard/writeups", description="Le dépôt contenant les writeups de la **Pynard** team", color=0xffa200)
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await infos_channel.send(embed=embed)

        await asyncio.sleep(day)
