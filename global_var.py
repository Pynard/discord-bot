
import os
import discord
from dotenv import load_dotenv

g_bot_token = '&'

g_channels =  {   'general' : 784498062303035404, 
                'flags'   : 786963650404941824 
            }

g_emoji = {   'hitler' : ':hitler:784774352838983691',
            'stalin' : ':stalin:784814367698976788',
            'darmanin' : ':darmanin:784847811732439040',
            'macron' : ':macron:784920050544017429'
        }

g_time_convert = { 'd':24*3600, 'h':3600, 'm':60, 's':1 }

g_big_numbers = {   '1': ':one:',
                    '2': ':two:',
                    '3': ':three:',
                    '4': ':four:',
                    '5': ':five:',
                    '6': ':six:',
                    '7': ':seven:',
                    '8': ':eight:',
                    '9': ':nine:',
                    '0': ':zero:' }

client = discord.Client()
