import discord
from datetime import datetime, timedelta
from discord.ext import commands
import random
import asyncio


#Utils

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong!')
    
    @commands.command()
    async def userid(self,ctx,member : discord.Member):
        await ctx.send(f'{ctx.message.author.id} is who sent the message and {member.id} is the tagged person' )


    @commands.command()
    async def trade(self,ctx,role: discord.Role,member : discord.Member,roleOther: discord.Role):
        if ((role in ctx.message.author.roles) and (roleOther in member.roles)):    
            await ctx.send(f'{ctx.message.author.mention} wants to trade {role} to {member.mention} for {roleOther}')
            await ctx.send(f'{member.mention} do you accept? (Yes/No). You have 30 seconds to accept')
            try:
                msg = await self.client.wait_for(
                    "message",
                    timeout = 30,
                    check=lambda message: message.author == member \
                        and message.channel == ctx.channel 
                )
                msg = msg.content.strip().lower()
                if msg == 'yes':
                    await ctx.message.author.add_roles(roleOther)
                    await member.add_roles(role)
                    await ctx.message.author.remove_roles(role)
                    await member.remove_roles(roleOther)
                    await ctx.send(f'Trade Completed!')
                elif msg == 'no':
                    await ctx.send(f'Trade Rejected!')
                else:
                    await ctx.send(f'Invalid input. Trade Rejected')

            except asyncio.TimeoutError:
                await ctx.send(f'Cancelling due to time out ') 
        else:
            await ctx.send(f'You or the user you want to trade with does not have the role listed in the trade')   

    @commands.command()
    @commands.cooldown(1,43200, commands.BucketType.user)
    async def collect(self,ctx):
        # rolesList = ['Santa Dodo', 'Elf Dodo', 'Frosty The Snowman Dodo', 'Gift Dodo', 'Grinch Dodo','Reindodo','Conductor Dodo']
        # roleAssign = random.choices(rolesList, weights = [5,5,10,30,30,10,10])[0]
        # role = discord.utils.get(ctx.guild.roles, name= str(roleAssign))
        # await ctx.message.author.add_roles(role)
        # await ctx.send(f'You have drawn the {role} role! Your next chance to role is in 12 hours')
        await ctx.send(f'This command is under maintenance until the database is completed')   


    @collect.error
    async def collect_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            if hours != 0:
                await ctx.send(f'Try again in {hours} hours and {minutes} minutes')
            else:
                await ctx.send(f'Try again in {minutes} minutes')

    @commands.command()
    async def roles(self,ctx):
        await ctx.send(f'This command is under maintenance until the database is completed')   
        # embed=discord.Embed(title="Collectable Roles List" , color=0xe392fe)
        # embed.add_field(name="Grinch Dodo - 30%", value="Show off your cranky side and dislike of christmas", inline=False)
        # embed.add_field(name="Gift Dodo - 30%", value="Be the gift that we need", inline=False)
        # embed.add_field(name="Reindodo - 10%", value="Choosen Dodo to lead the sleigh", inline=False)
        # embed.add_field(name="Conductor Dodo - 10%", value="The train to the mysterious dodo server", inline=False)
        # embed.add_field(name="Frosty The Snowman Dodo - 10%", value="Frosty the Snowdodo was a jolly happy soul", inline=False)
        # embed.add_field(name="Elf Dodo - 5%", value="Buddy The Elf Dodo!", inline=False)
        # embed.add_field(name="Santa Dodo - 5%", value="Secret Santa", inline=False)
        # await ctx.send(embed=embed)

#setup
def setup(client):
    client.add_cog(Utilities(client))