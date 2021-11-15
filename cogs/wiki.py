
from pywikiapi import wikipedia
from discord.ext import commands
import discord
import pymongo
import os

class cog_wiki(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.wiki = wikipedia("mcdiscontinued", "miraheze")
        self.wiki.login(os.environ.get("WIKI_USERNAME"), os.environ.get("WIKI_PASSWORD"))
        mongodb = pymongo.MongoClient(os.environ.get("DB_TOKEN"))
        self.db = mongodb.mc

        # Customise how the embed looks
        self.thumbnail_image = "https://static.miraheze.org/mcdiscontinuedwiki/6/60/Wiki_Icon.png"
        self.embed_color = 0x407467


    @commands.Cog.listener()
    async def on_message(self, message):

        # Discord role IDs
        editor_role = 843358516936704042
        loyalty_role = 868373753191628830
        addict_role = 868373926407966730

        # Embed colour values
        edit_colour = 0x2daf32
        create_colour = 0x36a1e8
        delete_colour = 0xe83535
        move_colour = 0xd635e8

        # Embed emoji text values
        edit_emoji = '📝'
        create_emoji = '📄'
        delete_emoji = '❌'
        move_emoji = '➡'
        
        # Try and get embed description
        try:
            description = message.embeds[0].description

            # For new pages
            if description[0] == create_emoji:
                wiki_page = description.split('has created article [')[1].split(']')[0]
                channel = self.client.get_channel(787102130871861288)
                await channel.send(f"The page {wiki_page.replace('_', ' ')} was created! check it out here: https://mcdiscontinued.miraheze.org/wiki/{wiki_page.replace(' ', '_')}")
                return

            # For edits
            if description[0] == edit_emoji:
                wiki_name = description.split('[')[1].split(']')[0]
                db_request = list(self.db.users.find({'wiki_name': wiki_name}))
                
                # Wiki user doesn't exist in the database
                if len(db_request) == 0:
                    return

                # Update database by querying wiki for editcount
                request = list(self.wiki.query(list="users", ususers=wiki_name, usprop="editcount"))[0]
                editcount = request['users'][0]['editcount']
                self.db.users.update_one({'wiki_name': wiki_name}, {'$set': {'editcount': editcount}})

                # Update roles
                member = await message.guild.fetch_member(db_request[0]['discord_id'])
                
                if db_request[0]['editcount'] >= 25:
                    role = message.guild.get_role(843358516936704042)
                    await member.add_roles(role)

                if db_request[0]['editcount'] >= 1000:
                    role = message.guild.get_role(loyalty_role)
                    await member.add_roles(role)

                if db_request[0]['editcount'] >= 5000:
                    role = message.guild.get_role(addict_role)
                    await member.add_roles(role)

                return

        except (IndexError, TypeError):
            return


    @commands.command(name="leaderboard", aliases=["top"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def top(self, ctx, sort="editcount", limit=15, reverse=False):
        
        # Make into something closer to what is expected
        sort = sort.lower()
        reverse = bool(reverse)
        
        # Make sure its a valid sort
        if not sort in ["editcount", "registration"]:
            await ctx.send("Invalid sort! see `%help leaderboard` for valid arguments")
            return
        
        # Query and sort all users who have an edit
        all_users = list(self.wiki.query(list="allusers", auprop="editcount|registration", aulimit=500, auwitheditsonly=True))[0]['allusers']
        sorted_users = sorted(all_users, key=lambda d: d[sort], reverse=not(reverse)) # not reverse to make it more relevant
        
        # Iterate through users to make the description pretty
        description = ""
        for place, user in enumerate(sorted_users[0:limit]):
            description += f"{place+1}. {user['name']}: {user[sort]}\n"
        
        # Create and send embed
        embedVar = discord.Embed(color=self.embed_color, title=f"Top Wiki Editors by {sort.title()}:", description=description)
        await ctx.send(embed=embedVar)
        
        
    @commands.command(name="user", aliases=[])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def user(self, ctx, user=None):
        
        # Check if user has been specified a user, then search database for them
        if user == None:
            db_request = list(self.db.users.find({'discord_id': ctx.author.id}))

            if len(db_request) == 0:
                await ctx.send(f"Please specify a user! Otherwise, register with the bot with `%linkaccount`.")
                return
            
            # Set user to wiki name of registered user
            user = db_request[0]['wiki_name']

        # Check if a user was mentioned
        elif user[0:3] == "<@!" and user[-1] == ">":
            db_request = list(self.db.users.find({'discord_id': int(user[3:-1])}))
            
            if len(db_request) == 0:
                await ctx.send(f"That user has not registered with the bot yet.")
                return
            
            # Set user to wiki name of registered user
            user = db_request[0]['wiki_name']

        # Query user
        request = list(self.wiki.query(list="users", ususers=user, usprop="editcount|registration|groups"))[0]
        
        # Ff this fails then the user doesn't exist
        try:
            embedVar = discord.Embed(color=self.embed_color, title=f"Stats for {request['users'][0]['name']}")
            embedVar.add_field(name="Wiki Registration Date", value=request['users'][0]['registration'], inline=False)
            embedVar.add_field(name="Edit Count", value=request['users'][0]['editcount'], inline=False)
            embedVar.add_field(name="Groups", value=", ".join(request['users'][0]['groups']), inline=False)

            await ctx.send(embed=embedVar)
        
        # Other wise send does not exist error
        except KeyError:
            await ctx.send("That user doesn't exist!")
            
        
    @commands.command(name="page", aliases=[])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def page(self, ctx, *, page=None):
        
        # Check if user has specified a page
        if page == None:
            await ctx.send("Please specify a page!")
            return
        
        # Query search
        request = list(self.wiki.query(list="search", srnamespace="*", srsearch=page, srlimit=1, srwhat="title"))[0]
        
        # Send the page
        try:
            await ctx.send(f"https://mcdiscontinued.miraheze.org/wiki/{request['search'][0]['title'].replace(' ', '_')}")
        
        # If it doesn't exist then send no page found
        except (KeyError, IndexError):
            await ctx.send("No page like that exists!")
            
            
    @commands.command(name="linkaccount", aliases=["link"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def link(self, ctx, user=None):

        # If a user isnt specified
        if user == None:
            await ctx.send("Please specify a wiki user to link to!")
            return

        # Wikis capitalise only the first letter
        user = user[0].upper() + user[1:]

        # Check if wiki user in the database
        db_request = list(self.db.users.find({'wiki_name': user}))

        if len(db_request) > 0:
            await ctx.send(f"{user} has already registered with the bot! If this was a mistake, please contact the mods so they can fix this for you.")
            return

        # Check if discord user in the database
        db_request = list(self.db.users.find({'discord_id':ctx.author.id}))

        if len(db_request) > 0:
            await ctx.send(f"You have already registered with the bot! If this was a mistake, please contact the mods so they can fix this for you.")
            return

        # Make sure user exists on the wiki
        request = list(self.wiki.query(list="users", ususers=user, usprop="editcount"))[0]

        # If this fails then the user doesn't exist
        try:
            wiki_name = request['users'][0]['name']
            editcount = request['users'][0]['editcount']

        except KeyError:
            await ctx.send("That user doesn't exist!")
            return

        # Create and store user dict in db
        user_dict = {
            'discord_id': ctx.author.id,
            'discord_name': ctx.author.name,
            'wiki_name': wiki_name,
            'editcount': editcount,
        }
        
        self.db.users.insert_one(user_dict)

        await ctx.send(f"Linked discord user {ctx.author.name} to wiki user {wiki_name}!")
        
        
def setup(bot):
    bot.add_cog(cog_wiki(bot))