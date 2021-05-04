import discord
from discord.ext import commands
import mysql
import os

# Roles List
rolesList = ['Dodo Red', 'Dodo Orange', 'Dodo Yellow', 'Dodo Spring', 'Dodo Matcha', 'Dodo Mint', 'Dodo Green',
             'Dodo Ice', 'Dodo Bbblu', 'Dodo Teal', 'Dodo Copyright', 'Dodo Cyan', 'Dodo Blue', 'Dodo Lavender',
             'Dodo Grape', 'Dodo Purple', 'Dodo Rose', 'Dodo Pink', 'Dodo Salmon', 'Dodo Special', 'Dodo Taffy',
             'Dodo Oak', 'Dodo Snow', 'Dodo Black', 'Dodo Gold']
activateRoles = ['Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Copyright', 'Cyan', 'Blue', 'Grape', 'Purple', 'Rose',
                 'Pink', 'Salmon', 'Spring', 'Matcha', 'Mint', 'Ice', 'Bbblu', 'Lavender', 'Special', 'Taffy', 'Oak',
                 'Snow', 'Black', 'Gold']


# Mentions
class Interactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['wave'])
    async def waves(self, ctx, member: discord.Member):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{ctx.message.author.mention} waves to {member.mention}")
        await ctx.send("https://media.tenor.com/images/ba69533b59d3ceaae8775a0550ff8037/tenor.gif")

    @waves.error
    async def waves_error(self, ctx, error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to wave at")
        await channel.send(f"{ctx.message.author} experienced a error using wave")

    @commands.command(aliases=['hug'])
    async def hugs(self, ctx, member: discord.Member):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg hug to {member.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugs.error
    async def hugs_error(self, ctx, error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to hug")
        await channel.send(f"{ctx.message.author} experienced a error using hug")

    @commands.command(aliases=['hugRole', 'hugsrole', 'grouphug'])
    async def hugsRole(self, ctx, role: discord.Role):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg group hug to {role.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugsRole.error
    async def hugsRole_error(self, ctx, error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a role to give a group hug to")
        await channel.send(f"{ctx.message.author} experienced a error using grouphug")

    @commands.command(aliases=['waveRole', 'waverole', 'groupwave'])
    async def wavesRole(self, ctx, role: discord.Role):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{ctx.message.author.mention} waves to {role.mention}")
        await ctx.send("https://media4.giphy.com/media/3pZipqyo1sqHDfJGtz/200.gif")

    @wavesRole.error
    async def wavesRole_error(self, ctx, error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occurred. Make sure you have mentioned a role to wave at a group")
        await channel.send(f"{ctx.message.author} experienced a error using wavesRole")

    @commands.command(aliases=["bringpeace"])
    async def banAlly(self, ctx):
        await ctx.send('Yes let us ban Ally!! Let us also ban Kyle!!')

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        embed_description = "**Role Information** \n"
        user = str(member.id)

        for role in activateRoles:
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {member.id}

        """)
            role_count = ''.join(map(str, c.fetchall()[0]))
            embed_description = embed_description + role_count + " Dodo " + role + " roles" + "\n"
        embed = discord.Embed(title=member.display_name + "'s Information", description=embed_description,
                              color=0xe392fe)
        embed.set_thumbnail(url=member.avatar_url)

        c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {member.id}

        """)
        money = ''.join(map(str, c.fetchall()[0]))
        c.execute(f"""SELECT birthday
                        FROM dodos
                        WHERE id = {member.id}

        """)
        birthday = ''.join(map(str, c.fetchall()[0]))
        embed.add_field(name=f"Money Balance", value=f"{money}", inline=True)
        if birthday == '0' or birthday == '0000':
            embed.add_field(name=f"Birthday", value=f"N/A", inline=True)
        else:
            embed.add_field(name=f"Birthday", value=f"{birthday}", inline=True)
        await ctx.send(embed=embed)
        c.close()
        db.close()

    @info.error
    async def info_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Error Occurred. Make sure you have mentioned a user")
        await channel.send(f"{ctx.message.author} experienced a error using info. {error}")


def setup(client):
    client.add_cog(Interactions(client))
