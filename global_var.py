
import os
import discord

g_bot_token = '&'
g_data_dir = "data"
g_local_dir = "local"
g_dump_dir = "dump"

g_devs = ['maxigir','lsorignet']

# Pynard guild
g_guild = 784498061857521675

g_channels =  { 'general' : 784498062303035404,
                'infos'   : 786965162703192084,
                'voice'   : 784498062303035405,
                'goulag'  : 797809790394695700 }

g_roles = { 'goulag' : 785940566784999455 }

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
