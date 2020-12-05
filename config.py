
import os
import discord
from dotenv import load_dotenv

bot_token = '&'

channels =  {   'general' : 784498062303035404, 
                'flags'   : 784818974960517160
            }

emoji = {   'hitler' : ':hitler:784774352838983691',
            'stalin' : ':stalin:784814367698976788',
            'darmanin' : ':darmanin:784847811732439040'
        }



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
