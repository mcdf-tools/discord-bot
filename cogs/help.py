
from discord.ext import commands
import discord, json

# Customise how the embed looks
footer_text = "MC Discontinued Test Bot"
thumbnail_image = "https://static.miraheze.org/mcdiscontinuedwiki/2/24/Main_Page_Logo_%282021_Update%29.png"
embed_color = 0x407467

class cog_help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.help = json.load(open(f"help.json", 'r'))

    @commands.command(name="help", aliases=[])
    async def help(self, ctx, command=None):

        # If no specific command was chosen
        if command == None:
            embedVar = discord.Embed(color=embed_color, title="Command List:")
            
            for help in self.help:
                embedVar.add_field(name=help['usage'], value=help['desc'], inline=False)

            # send embed
            embedVar.set_thumbnail(url=thumbnail_image)
            embedVar.set_footer(text=footer_text)
            await ctx.send(embed=embedVar)

        # For specific commands
        else:
            for help in self.help:
                if command == help['name'] or command in help['aliases']:
                    embedVar = discord.Embed(color=embed_color, title=help['usage'], description=help['desc'])
                    embedVar.add_field(name="Aliases", value=f"`{'` `'.join(help['aliases'])}`" if len(help['aliases']) else "None", inline=False)
                    embedVar.add_field(name="Required Arguments", value=help['required'], inline=False)
                    embedVar.add_field(name="Optional Arguments", value=help['optional'], inline=False)

                    # send embed
                    embedVar.set_thumbnail(url=thumbnail_image)
                    embedVar.set_footer(text=footer_text)
                    await ctx.send(embed=embedVar)
        
        
    @commands.command(name="wiki", aliases=[])
    async def wiki(self, ctx):
        embedVar = discord.Embed(color=embed_color, title="MC Disontinued Wiki Info")
        embedVar.add_field(name="Wiki", value="https://mcdiscontinued.miraheze.org/", inline=False)
        embedVar.add_field(name="Discord", value="https://discord.gg/n7v7pgE", inline=False)
        embedVar.add_field(name="Github", value="https://github.com/Minecraft-Discontinued-Features/", inline=False)
        embedVar.set_thumbnail(url=thumbnail_image)
        embedVar.set_footer(text=footer_text)
        await ctx.send(embed=embedVar)
        

def setup(bot):
    bot.add_cog(cog_help(bot))