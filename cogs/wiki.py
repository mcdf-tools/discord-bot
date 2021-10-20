
from pywikiapi import wikipedia
from discord.ext import commands
import discord

class cog_wiki(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.wiki = wikipedia("mcdiscontinued", "miraheze")
        self.db = None # TODO: replace with some kind of database (mongodb?)


    @commands.command(name="leaderboard", aliases=["top"])
    async def top(self, ctx, sort="editcount", reverse=False):
        
        # make into something closer to what is expected
        sort = sort.lower()
        reverse = bool(reverse)
        
        # make sure its a valid sort
        if not sort in ["editcount", "registration"]:
            await ctx.send("Invalid sort! see `%help leaderboard` for valid arguments")
            return
        
        # query and sort all users who have an edit
        all_users = list(self.wiki.query(list="allusers", auprop="editcount|registration", aulimit=500, auwitheditsonly=True))[0]['allusers']
        sorted_users = sorted(all_users, key=lambda d: d[sort], reverse=not(reverse)) # not reverse to make it more relevant
        
        # iterate through users to make the description pretty
        description = ""
        for place, user in enumerate(sorted_users[0:15]):
            description += f"{place+1}. {user['name']}: {user[sort]}\n"
        
        # create and send embed
        embedVar = discord.Embed(color=0xFFFFFF, title=f"Top Wiki Editors by {sort.title()}:", description=description)
        await ctx.send(embed=embedVar)
        
        
    @commands.command(name="user", aliases=[])
    async def user(self, ctx, user=None):
        
        # check if user has been specified a user
        # TODO: make it so if no user is specified use the linked user
        if user == None:
            await ctx.send("Please specify a user!")
            return
        
        # query user
        request = list(self.wiki.query(list="users", ususers=user, usprop="editcount|registration|gender|groups"))[0]
        
        # if missing key exists, then that user doesn't exist
        try:
            request['users'][0]['missing']
            await ctx.send("That user doesn't exist!")
            return
        
        # otherwise create and send embed with prop values
        except KeyError:
            embedVar = discord.Embed(color=0xFFFFFF, title=f"Stats for {request['users'][0]['name']}")
            embedVar.add_field(name="Wiki Registration Date", value=request['users'][0]['registration'], inline=False)
            embedVar.add_field(name="Edit Count", value=request['users'][0]['editcount'], inline=False)
            embedVar.add_field(name="Gender", value=request['users'][0]['gender'], inline=False)
            embedVar.add_field(name="Groups", value=", ".join(request['users'][0]['groups']), inline=False)
            await ctx.send(embed=embedVar)
            
        
    @commands.command(name="page", aliases=[])
    async def page(self, ctx, *, page=None):
        
        # check if user has specified a page
        if page == None:
            await ctx.send("Please specify a page!")
            return
        
        # query search
        request = list(self.wiki.query(list="search", srnamespace="*", srsearch=page, srlimit=1, srwhat="title"))[0]
        print(request)
        
        # send the page
        try:
            await ctx.send(f"https://mcdiscontinued.miraheze.org/wiki/{request['search'][0]['title'].replace(' ', '_')}")
        
        # if it doesn't exist then send no page found
        except (KeyError, IndexError):
            await ctx.send("No page like that exists!")
            
            
    @commands.command(name="link", aliases=[])
    async def link(self, ctx, user=None):

        if user == None:
            await ctx.send("Please specify a user!")
            return
        
        await ctx.send(f"Unsucessfully linked {user}!")
        
        
        
def setup(bot):
    bot.add_cog(cog_wiki(bot))