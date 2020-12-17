
from global_var import *
import os
import requests

def help_cmd(cmd):
    return f"{g_bot_token}{Command.__dict__[cmd].__doc__}"


def mkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(url, filename):
    f = requests.get(url)
    file = open(filename, 'wb')
    file.write(f.content)
    file.close()