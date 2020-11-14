import discord
from discord.ext import commands
import time

#Utils
class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @commands.command()
    async def ping(ctx):
        await ctx.send(f'Pong! {round(client.latency*1000)}ms')
        
    @commands.command(aliases = ['remindme'])
    async def reminder(ctx, rtime, *, reminder):
        await ctx.message.delete(delay = 0)
        await ctx.send(f"{ctx.message.author.mention} reminder has been set")
        time.sleep(int(rtime))
        await ctx.send(f"{ctx.message.author.mention} here is your reminder to {reminder}")

def setup(client):
    client.add_cog(Utilities(client))