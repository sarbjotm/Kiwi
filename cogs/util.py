import discord
from discord.ext import commands
import random

#Utils
class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong!')
    
    @commands.command()
    @commands.cooldown(1,86400, commands.BucketType.user)
    async def collect(self,ctx):
        roles = ['Santa Dodo', 'Elf Dodo', 'Frosty The Snow Dodo', 'Gift Dodo', 'Grinch Dodo']
        roleAssign = random.choices(roles, weights = [5,5,10,30,50])[0]
        await ctx.message.author.add_roles(roleAssign)
        await ctx.send(f'You have drawn the {roleAssign[0]} role! Your next chance to role is in 24 hours')

    @collect.error
    async def collect_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            await ctx.send(f'Try again in {hours:.2f} hours and {minutes:.2f} minutes')
             
#setup
def setup(client):
    client.add_cog(Utilities(client))