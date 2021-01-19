
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

        ### HISTORY
        #history = [ [ col.text for col in line.findAll('td') ][1:] for line in soup.find(name='table', attrs={'class':'table table-striped'}).findAll('tr')[1:] ]
        history = [ [ [ col.text for col in line.findAll('td') ][1:] for line in year ] for year in [ year.findAll('tr')[1:] for year in soup.findAll(name='table', attrs={'class':'table table-striped'}) if "PlaceEvent" in year.text ] ]
        #ctf_href = [ line.find('a')['href'] for line in soup.find(name='table', attrs={'class':'table table-striped'}).findAll('tr')[1:] ]
        ctf_href = [ [ line.find('a')['href'] for line in year ] for year in [ year.findAll('tr')[1:] for year in soup.findAll(name='table', attrs={'class':'table table-striped'}) if "PlaceEvent" in year.text ] ]

        embed = discord.Embed(title='History', color=0xffa200)
        embed.add_field(name=':triangular_flag_on_post: CTF', value='** **', inline=True)
        embed.add_field(name=':trophy: Rank', value='** **', inline=True)
        embed.add_field(name=':game_die: Points', value='** **', inline=True)

        for history_year,ctf_href_year in zip(history[::-1],ctf_href[::-1]):
            for (rank,name,_,points),href in zip(history_year[::-1],ctf_href_year[::-1]):
                html_text = requests.get('https://ctftime.org'+href, headers={'User-Agent': 'Mozilla/5.0'}).text
                soup = BeautifulSoup(html_text,'html.parser')
                total_teams = soup.findAll(name='td', attrs={'class':'place'})[-1].text
                embed.add_field(name=name, value='** **', inline=True)
                embed.add_field(name=f'{rank}/{total_teams}', value='** **', inline=True)
                embed.add_field(name=points, value='** **', inline=True)

        await infos_channel.send(embed=embed)

        await asyncio.sleep(day)
