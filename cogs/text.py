import discord
from discord.ext import commands

#Text Alterations
class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spongebob(self,ctx, *, message):
        new = list(message)
        for i in range(0,len(new)):
            if( i % 2 == 0):
                new[i] = new[i].upper()
                "".join(new[i])
            else:
                new[i] = new[i].lower()
                "".join(new[i])
        str1 = ''
        for i in new:
            str1 += i 
        await ctx.send(f"{str1}")
    
    @spongebob.error
    async def spongebob_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,spongebob Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using spongebob")  

    @commands.command(aliases = ["fw","sparkles"])
    async def fireworks(self,ctx, *, message):
        emoji = "✨"
        messageList = message.split()
        fireworkString = emoji
        for i in range(0, len(messageList)):
            fireworkString += (messageList[i] + emoji)
        await ctx.send(f"{fireworkString}")
    
    @fireworks.error
    async def fireworks_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,fireworks Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using fireworks")  

    @commands.command(aliases = ["sp","space","spaces"])
    async def spaced(self,ctx, *, message):
        noSpaceString = message.replace(" ", "")
        spacedString = ""
        for i in range(0, len(noSpaceString)):
            spacedString += noSpaceString[i]
            spacedString += " "
        await ctx.send(f"{spacedString}")
    
    @spaced.error
    async def spongebob_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,spaced Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using spaced")  

def setup(client):
    client.add_cog(Text(client))