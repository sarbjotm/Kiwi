import discord
from discord.ext import commands
import os

# Text Alterations
class Text(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def spongebob(self, ctx, *, message):
        new = list(message)
        for i in range(0, len(new)):
            if i % 2 == 0:
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
    async def spongebob_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,spongebob Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using spongebob")

    @commands.command(aliases=["fw", "sparkles"])
    async def fireworks(self, ctx, *, message):
        emoji = "✨"
        message_list = message.split()
        firework_string = emoji
        for i in range(0, len(message_list)):
            firework_string += (message_list[i] + emoji)
        await ctx.send(f"{firework_string}")

    @fireworks.error
    async def fireworks_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,fireworks Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using fireworks. {error}")

    @commands.command(aliases=["sp", "space", "spaces"])
    async def spaced(self, ctx, *, message):
        no_space_string = message.replace(" ", "")
        spaced_string = ""
        for i in range(0, len(no_space_string)):
            spaced_string += no_space_string[i]
            spaced_string += " "
        await ctx.send(f"{spaced_string}")

    @spaced.error
    async def spaced_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,spaced Some Random Text**")
        await channel.send(f"{ctx.message.author} experienced a error using spaced")


def setup(client):
    client.add_cog(Text(client))
