import discord
from datetime import datetime, timedelta
from discord.ext import commands
import random
import sqlite3
import asyncio


#Utils


class Utilities(commands.Cog):
    conn = sqlite3.connect('members.db')
    c = conn.cursor()

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
    @commands.cooldown(1,10, commands.BucketType.user)
    async def collect(self,ctx):
        rolesList = ['Dodo Red','Dodo Orange']
        roleAssign = random.choices(rolesList, weights = [1,1])[0]
        role = discord.utils.get(ctx.guild.roles, name= str(roleAssign))
        await ctx.message.author.add_roles(role)
        await ctx.send(f'You have drawn the {role} role! Your next chance to role is in 24 hours')
        role = str(role)
        role = role.split()[1]
        c.execute(f"""SELECT {role} 
                    FROM dodos 
                    WHERE id='{ctx.message.author.id}'
                """)
        c.execute(f"""UPDATE dodos 
                  SET {role} = {c.fetchone()[0]} + 1 
                  WHERE id='{ctx.message.author.id}'
            """)
        conn.commit()
        c.execute(f"""SELECT {role} 
                    FROM dodos 
                    WHERE id='{ctx.message.author.id}'
                """)
        await ctx.send(f'You now have {c.fetchone()[0]} {role} roles')  
        await ctx.send(f'test message') 


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
    async def activate(self,ctx,role: discord.Role):
        activateRoles = ['Red','Orange','Yellow','Green','Teal','Copyright','Bluev2','Blue','Purplev2','Purple','Pinkv2','Pink']
        if (role in ctx.message.author.roles):
            for r in activateRoles:
                try:
                    roleRemove = discord.utils.get(ctx.guild.roles, name=r)
                    await ctx.message.author.remove_roles(roleRemove)
                except:
                    pass
            role = str(role)
            role = role.split()[1]
            roleAssign = discord.utils.get(ctx.guild.roles, name=role)
            
            await ctx.message.author.add_roles(roleAssign)
        else:
            await ctx.send("You do not have that role")



    @commands.command()
    async def roles(self,ctx):
        embed=discord.Embed(title="Collectable Roles List" , color=0xe392fe)
        embed.add_field(name="Dodo Red", value="Red colouring", inline=False)
        embed.add_field(name="Dodo Orange", value="Orange colouring", inline=False)
        embed.add_field(name="Dodo Yellow", value="Yellow colouring", inline=False)
        embed.add_field(name="Dodo Green", value="Green colouring", inline=False)
        embed.add_field(name="Dodo Teal", value="Teal colouring", inline=False)
        embed.add_field(name="Dodo Copyright", value="Some sort of blue", inline=False)
        embed.add_field(name="Dodo Bluev2", value="Bluev2 colouring", inline=False)
        embed.add_field(name="Dodo Blue", value="Blue colouring", inline=False)
        embed.add_field(name="Dodo Purplev2", value="Purplev2 colouring", inline=False)
        embed.add_field(name="Dodo Purple", value="Purple colouring", inline=False)
        embed.add_field(name="Dodo Pinkv2", value="Pinkv2 colouring", inline=False)
        embed.add_field(name="Dodo Pink", value="Pink colouring", inline=False)
    
        await ctx.send(embed=embed)

#setup
def setup(client):
    client.add_cog(Utilities(client))