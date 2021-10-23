
from pywikiapi import wikipedia
from discord.ext import commands
import discord
import pymongo

class cog_wiki(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.wiki = wikipedia("mcdiscontinued", "miraheze")
        self.wiki.login("UnobtainedBot", "kJuBFJQsX27NR7y")
        mongodb = pymongo.MongoClient("mongodb+srv://user:y8QOlhZ60VIexhKd@mcdiscontinued.qhbkk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = mongodb.mc

    def getTokens(self, type="csrf"):
        return list(self.wiki.query(meta="tokens", type=type))[0].tokens

    @commands.command(name="leaderboard", aliases=["top"])
    async def top(self, ctx, sort="editcount", limit=15, reverse=False):
        
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
        for place, user in enumerate(sorted_users[0:limit]):
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
        request = list(self.wiki.query(list="users", ususers=user, usprop="editcount|registration|groups"))[0]
        
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

        # if a user isnt specified
        if user == None:
            await ctx.send("Please specify a wiki user to link to!")
            return

        # wikis capitalise only the first letter
        user = user[0].upper() + user[1:]

        # check if wiki user in the database
        db_request = list(self.db.users.find({'wiki_name': user}))

        if len(db_request) > 0:
            await ctx.send(f"{user} has already registered with the bot! If this was a mistake, please contact the mods so they can fix this for you.")
            return

        # check if discord user in the database
        db_request = list(self.db.users.find({'discord_id':ctx.author.id}))

        if len(db_request) > 0:
            await ctx.send(f"You have already registered with the bot! If this was a mistake, please contact the mods so they can fix this for you.")
            return

        # make sure user exists on the wiki
        request = list(self.wiki.query(list="users", ususers=user))[0]

        # if missing key exists, then that user doesn't exist
        try:
            request['users'][0]['missing']
            await ctx.send("That user doesn't exist!")
            return

        except:
            wiki_name = request['users'][0]['name']

        # create and store user dict in db
        user_dict = {
            'discord_id': ctx.author.id,
            'discord_name': ctx.author.name,
            'wiki_name': wiki_name,
        }
        
        self.db.users.insert_one(user_dict)

        await ctx.send(f"Linked discord user {ctx.author.name} to wiki user {wiki_name}!")
        
        
def setup(bot):
    bot.add_cog(cog_wiki(bot))