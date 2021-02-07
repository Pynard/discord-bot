
import asyncio
import requests
import json
from bs4 import BeautifulSoup

from global_var import *
from command.ctf.utils import parse_url

async def update_planning():
    await client.wait_until_ready()

    day = 3600*24
    planning_channel = client.get_channel(g_channels['planning'])

    while not client.is_closed():
        planning_data = dl_planning()

        await planning_channel.purge()
        for ctf in planning_data:
            embed,infos,_,_ = parse_url(ctf['ctftime_url'])
            await planning_channel.send(embed=embed)
            for title,text in infos.items():
                await planning_channel.send(title)
                await planning_channel.send(text)
            await planning_channel.send('```ini\n[ Votez pour moi ! ]\n```')
            await planning_channel.send('** **')
            await planning_channel.send('** **')
            await planning_channel.send('** **')

        await asyncio.sleep(day)

def dl_planning():
    html_text = requests.get('https://ctftime.org/api/v1/events/?limit=3', headers={'User-Agent': 'Mozilla/5.0'}).text
    return json.loads(html_text)

def load_planning(name):
    return pickle.load(open(g_data_dir+f'/planning','rb'))

def save_planning(name,content):
    pickle.dump(content,open(g_data_dir+f'/planning','wb'))
