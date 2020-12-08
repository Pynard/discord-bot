
from global_var import *

def help_cmd(cmd):
    return f"{g_bot_token}{Command.__dict__[cmd].__doc__}"


