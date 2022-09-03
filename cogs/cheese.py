from discord.ext import commands
import discord

class cog_cheese(commands.Cog):

    def __init__(self, client):

        self.client = client
        
    @commands.command(name="cheese", aliases=["ILoveCheese"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cheese(self, ctx):
      member = await message.guild.fetch_member(db_request[0]['discord_id'])
      role = message.guild.get_role(editor_role)
      await member.add_roles(802013239289970690)

async def setup(bot):
    await bot.add_cog(cog_cheese(bot))
