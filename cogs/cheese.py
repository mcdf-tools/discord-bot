from discord.ext import commands
import discord

class cog_cheese(commands.Cog):

    def __init__(self, client):

        self.client = client
        
    @commands.command(name="cheese", aliases=["ILoveCheese"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ILoveCheese(self, ctx):
      member = await message.guild.fetch_member(db_request[0]['discord_id'])
      role = message.guild.get_role(802013239289970690)
      if role in member.roles:
        await member.remove_roles(role)
      else:
        await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(cog_cheese(bot))
