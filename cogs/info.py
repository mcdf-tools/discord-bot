
from discord.ext import commands
import discord, json

class cog_info(commands.Cog):

    def __init__(self, client):

        self.client = client

        # Customise how the embed looks
        self.footer_text = "Minecraft Discontinued Features Bot"
        self.thumbnail_image = "https://static.miraheze.org/mcdiscontinuedwiki/6/60/Wiki_Icon.png"
        self.embed_color = 0x407467
        
    @commands.command(name="info", aliases=["wiki"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wiki(self, ctx):

        # Create embed
        embedVar = discord.Embed(color=self.embed_color, title="MC Disontinued Wiki Info")
        embedVar.set_thumbnail(url=self.thumbnail_image)
        embedVar.set_footer(text=self.footer_text)

        # Add fields
        embedVar.add_field(name="Wiki", value="https://mcdiscontinued.miraheze.org", inline=False)
        embedVar.add_field(name="Discord", value="https://discord.gg/n7v7pgE", inline=False)
        embedVar.add_field(name="Test Wiki", value="https://mcdftestingwiki.miraheze.org", inline=False)
        embedVar.add_field(name="Github", value="https://github.com/Minecraft-Discontinued-Features", inline=False)
        #embedVar.add_field(name="Youtube", value="https://www.youtube.com/channel/UC8gg3Ak2a8PO0iiwv9I2eNA (plans for this account are currently on hold)", inline=False)
        embedVar.add_field(name="Reddit", value="https://www.reddit.com/r/DiscontinuedMC", inline=False)
        
        await ctx.send(embed=embedVar)
        

def setup(bot):
    bot.add_cog(cog_info(bot))