import discord
from discord.ext import commands

#Text Alterations
class Text(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

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

    @commands.command(aliases = ["fw"])
    async def fireworks(self,ctx, *, message):
        emoji = "✨"
        messageList = message.split()
        fireworkString = ""
        for i in range(0, len(messageList)):
            fireworkString += (messageList[i] + emoji)
        await ctx.send(f"{fireworkString}")

    @commands.command(aliases = ["sp","space","spaces"])
    async def spaced(self,ctx, *, message):
        noSpaceString = message.replace(" ", "")
        spacedString = ""
        for i in range(0, len(noSpaceString)):
            spacedString += noSpaceString[i]
            spacedString += " "
        await ctx.send(f"{spacedString}")

def setup(client):
    client.add_cog(Text(client))