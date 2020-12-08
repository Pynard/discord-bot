
from global_var import * 

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

