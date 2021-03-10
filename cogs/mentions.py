import discord
import asyncio
from discord.ext import commands

#Mentions
class Interactions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['wave'])
    async def waves(self,ctx,member : discord.Member):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} waves to {member.mention}")
        await ctx.send("https://media.tenor.com/images/ba69533b59d3ceaae8775a0550ff8037/tenor.gif")
    
    @waves.error
    async def waves_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to wave at")
        await channel.send(f"{ctx.message.author} experienced a error using wave")  

    @commands.command(aliases = ['hug'])
    async def hugs(self,ctx,member : discord.Member):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg hug to {member.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugs.error
    async def hugs_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a user to hug")
        await channel.send(f"{ctx.message.author} experienced a error using hug") 

    @commands.command(aliases = ['hugRole','hugsrole','grouphug'])
    async def hugsRole(self,ctx,role : discord.Role):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} gibs beeeeg group hug to {role.mention}")
        await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

    @hugsRole.error
    async def hugsRole_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a role to give a group hug to")
        await channel.send(f"{ctx.message.author} experienced a error using grouphug") 

    @commands.command(aliases = ['waveRole','waverole','groupwave'])
    async def wavesRole(self,ctx,role : discord.Role):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} waves to {role.mention}")
        await ctx.send("https://media4.giphy.com/media/3pZipqyo1sqHDfJGtz/200.gif")
    
    @wavesRole.error
    async def wavesRole_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Make sure you have mentioned a role to wave at a group")
        await channel.send(f"{ctx.message.author} experienced a error using wavesRole") 

    @commands.command(aliases = ["bringpeace"])
    async def banAlly(self,ctx):
        await ctx.send('Yes let us ban Ally!! Let us also ban Kyle!!')

def setup(client):
    client.add_cog(Interactions(client))