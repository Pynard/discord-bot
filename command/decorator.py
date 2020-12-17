
from global_var import * 

def dev_only(func):
    async def wrapper(message):
        if message.author.name in g_devs:
            response = await func(message)
        else:
            response = f'**{message.author.name}** is not in the sudoers file. This incident will be reported.\nhttps://i.stack.imgur.com/sm7og.png'
        return response
    return wrapper

def error(func):
    async def wrapper(message):
        error = await func(message)
        if error:
            await message.channel.send(f'блят {message.author.mention} ! '+error+f'```{g_bot_token}{func.__doc__}```')
        return error
    return wrapper

def inplace(func):
    async def wrapper(message):
        response = await func(message)
        await message.delete()
        return response
    return wrapper

