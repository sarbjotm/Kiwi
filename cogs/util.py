import discord
from discord.ext import commands
import random

#Utils
class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(client.latency*1000)}ms')
    

    @commands.command()
    @commands.cooldown(1,1440, commands.BucketType.user)
    async def collect(self,ctx, member):
        roles = ['Santa Dodo', 'Elf Dodo', 'Frosty The Snow Dodo', 'Gift Dodo', 'Grinch Dodo']
        roleAssign = random.choice(roles, weights = [5,5,10,30,50])
        await ctx.send(f'You have drawn the {roleAssign} role! Your next chance to role is in 24 hours')
        await client.add_roles(member, roleAssign)
        
   
def setup(client):
    client.add_cog(Utilities(client))