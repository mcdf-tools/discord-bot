
from discord.ext import commands
import discord, os
from dotenv import load_dotenv

load_dotenv('.env')

# Initialise bot
bot = commands.Bot(command_prefix=os.environ.get("DISCORD_COMMAND_PREFIX"))
# We make our own help function
bot.remove_command('help') 

@bot.event
async def on_ready():
    # When ready state what guilds the bot is connected to
    print(f'{bot.user} is connected to the following guilds:')
    for guild in bot.guilds: 
        print(f'{guild.name} (id: {guild.id})')

@bot.event
async def on_disconnect():
    # If disconnected, state that it disconnected (likely due to internet down)
    print(f'{bot.user} has been disconnected')

@bot.event
async def on_command_error(ctx, error):
    # The command is on cooldown
    if isinstance(error, commands.CommandOnCooldown): 
        await ctx.send(f"{error}", delete_after=error.retry_after)
        return
    # The commmand is not found
    elif isinstance(error, commands.CommandNotFound):
        return
    # Something else broke
    else:
        await ctx.send(f"Something broke. Error:\n`{error}`")
        print(error)

def load_cogs():
    # load all cogs in the cogs directory
    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")

# Run bot
load_cogs()
bot.run(os.environ.get("DISCORD_TOKEN"))