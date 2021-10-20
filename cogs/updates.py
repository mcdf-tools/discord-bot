
from discord.ext import commands
import discord

class cog_updates(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        
        # edit colour = #2daf32 (📝)
        # create colour = #36a1e8 (📄)
        # deletion colour = #e83535 (❌)
        # moving colour = #d635e8 (➡)
        
        # try and get embed description
        try:
            description = message.embeds[0].description
        except IndexError:
            return
        
        # ugly way to get the page name
        if description[0] == "📄":
            for i in description.split(')'):
                if "has created article" in i:
                    pagename = i.split('=')[1]
                    
        # get #page-log channel and send to it
        channel = self.client.get_channel(787102130871861288)
        await channel.send(f"The page {pagename.replace('_', ' ')} was created! check it out here: https://mcdiscontinued.miraheze.org/wiki/{pagename}")
        
        
def setup(bot):
    bot.add_cog(cog_updates(bot))