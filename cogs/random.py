
from discord.ext import commands
import discord

class cog_random(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Reacts if it sees something in message
    @commands.Cog.listener()
    async def on_message(self, message):
    
        if "cheese" in message.content.lower():
            await message.add_reaction("🧀")
            
        if "villager" in message.content.lower():
            await message.channel.send("hrmm")
    

def setup(bot):
    bot.add_cog(cog_random(bot))