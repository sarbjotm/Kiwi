import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import sqlite3
import asyncio
from pathlib import Path
botfile = os.path.dirname(os.getcwd())
botfile = os.path.join(botfile, 'bot')
# from botfile import client


#TODO: Check if redeploying bot resets the database, if it does reclone heroku and get latest file before each commit

#Utils
d = Path(__file__).resolve().parents[1]
d = d/'members.db'
conn = sqlite3.connect(str(d))
c = conn.cursor()
rolesList = ['Dodo Red','Dodo Orange','Dodo Yellow','Dodo Green','Dodo Teal','Dodo Copyright','Dodo Cyan','Dodo Blue','Dodo Grape','Dodo Purple','Dodo Rose','Dodo Pink','Dodo Salmon']
activateRoles = ['Red','Orange','Yellow','Green','Teal','Copyright','Cyan','Blue','Grape','Purple','Rose','Pink','Salmon']

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
        if ((str(role) not in rolesList) or (str(roleOther) not in rolesList)):
            await ctx.send("Trade only collectable roles")
        elif ((role in ctx.message.author.roles) and (roleOther in member.roles)):    
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
                    #
                    c.execute(f"""
                        UPDATE dodos
                        SET {str(roleOther).split(" ")[1]} = {str(roleOther).split(" ")[1]} + 1
                        WHERE id = {ctx.message.author.id}

                    
                    """)
                    conn.commit()
                    c.execute(f"""
                        UPDATE dodos
                        SET {str(role).split(" ")[1]} = {str(role).split(" ")[1]} - 1
                        WHERE id = {ctx.message.author.id}

                    
                    """)

                    conn.commit()
                    await member.add_roles(role) #Add role (Make SQL Here)
                    #SQL
                    c.execute(f"""
                        UPDATE dodos
                        SET {str(role).split(" ")[1]} = {str(role).split(" ")[1]} + 1
                        WHERE id = {member.id}

                    """)
                    conn.commit()
                    c.execute(f"""
                        UPDATE dodos
                        SET {str(roleOther).split(" ")[1]} = {str(roleOther).split(" ")[1]} -1
                        WHERE id = {member.id}

                    """)
                    conn.commit()
                    #SQL HERE CHECK IF == 1 THEN REMOVE
                    c.execute(f"""
                        SELECT {str(role).split(" ")[1]}
                        FROM dodos
                        WHERE {ctx.message.author.id}
                    
                    
                    """)
                    if(int(c.fetchone()[0]) == 0):
                        await ctx.message.author.remove_roles(role)

                    c.execute(f"""
                        SELECT {str(roleOther).split(" ")[1]}
                        FROM dodos
                        WHERE {member.id}
                    
                    """)
                    if(int(c.fetchone()[0]) == 0):
                        await member.remove_roles(roleOther)
                    #SQL HERE
                    role = str(role)
                    role = role.split(" ")[1]
                    roleRemove = discord.utils.get(ctx.guild.roles, name=role)
                    await ctx.message.author.remove_roles(roleRemove)
                    roleOther = str(roleOther)
                    roleOther = roleOther.split()[1]
                    roleRemove = discord.utils.get(ctx.guild.roles, name=roleOther)
                    await member.remove_roles(roleRemove) 
                    
                    await ctx.send(f'Trade Completed!')
                    # channel = client.get_channel(800965152132431892)
                    # user = str(ctx.message.author)
                    # embed=discord.Embed(title= user + "'s Roles" , color=0xe392fe)
                    # embed.set_thumbnail(url=ctx.message.author.avatar_url)
                    # for role in activateRoles:
                    #     c.execute(f"""SELECT {role}
                    #                 FROM dodos
                    #                 WHERE id = {ctx.message.author.id}
                    #     """)
                    #     roleCount = str(c.fetchone()[0]) + " Dodo " + role + " roles"
                    #     embed.add_field(name=roleCount, value="Information about how many of this role you have", inline=False)
                    # await channel.send(embed=embed) 
                    # user = str(member)
                    # embed=discord.Embed(title= user + "'s Roles" , color=0xe392fe)
                    # embed.set_thumbnail(url=member.avatar_url)
                    # for role in activateRoles:
                    #     c.execute(f"""SELECT {role}
                    #                 FROM dodos
                    #                 WHERE id = {member.author.id}
                    #     """)
                    #     roleCount = str(c.fetchone()[0]) + " Dodo " + role + " roles"
                    #     embed.add_field(name=roleCount, value="Information about how many of this role you have", inline=False)
                    # await channel.send(embed=embed) 
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
        roleAssign = random.choices(rolesList, weights = [1,1,1,1,1,1,1,1,1,1,1,1,1])[0]
        print(roleAssign)
        role = discord.utils.get(ctx.guild.roles, name=roleAssign)
        await ctx.message.author.add_roles(role)
        await ctx.send(f'You have drawn the {role} role! To activate it use the ,activate \"{role}\" command. Your next chance to roll is in 12 hours')
        roleAssign = roleAssign.split(" ")
        try:
            c.execute(f"""UPDATE dodos
            SET {roleAssign[1]} = {roleAssign[1]} + 1
            WHERE id = {ctx.message.author.id}
            """)
        except:
            print("Error in adding role...")
        try:
            c.execute(f"""SELECT {roleAssign[1]} 
                        FROM dodos 
                        WHERE id='{ctx.message.author.id}'
                    """)
            conn.commit()
        except:
            print("Error in getting role")
        await ctx.send(f'You now have {c.fetchone()[0]} {str(role)} roles')
        channel = ctx.guild.get_channel(800965152132431892)
        user = str(ctx.message.author)
        embed=discord.Embed(title= user + "'s Roles" , color=0xe392fe)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        for role in activateRoles:
            c.execute(f"""SELECT {role}
                          FROM dodos
                          WHERE id = {ctx.message.author.id}
            """)
            roleCount = str(c.fetchone()[0]) + " Dodo " + role + " roles"
            embed.add_field(name=roleCount, value="Information about how many of this role you have", inline=False)
        await channel.send(embed=embed)    

    @collect.error
    async def collect_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            seconds %= 60
            if hours != 0:
                await ctx.send(f'Try again in {hours} hours {minutes} minutes and {int(seconds)} seconds')
            else:
                await ctx.send(f'Try again in {minutes} minutes and {seconds} seconds')
            await channel.send(f"{ctx.message.author} experienced a {error}")



    @commands.command()
    async def activate(self,ctx,role: discord.Role):
        if ((str(role) not in rolesList)):
            await ctx.send("Only can activate collected Colour Roles.")
            await ctx.send("Make sure you have provided the correct arguments. Roles are case senestive")
            await ctx.send("Example usage: ,activate \"Dodo Red\" ")
        elif (role in ctx.message.author.roles):
            for r in activateRoles:
                    roleRemove = discord.utils.get(ctx.guild.roles, name=r)
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                        break
            print(role)
            role = str(role)
            role = role.split()[1]
            print(role)
            roleAssign = discord.utils.get(ctx.guild.roles, name=role)
            await ctx.message.author.add_roles(roleAssign)
        
        else:
            await ctx.send("You do not have that role.")
            await ctx.send("Make sure you have provided the correct arguments. Roles are case senestive")
            await ctx.send("Example usage: ,activate \"Dodo Red\" ")
        

    @commands.command()
    async def myroles(self,ctx):
        user = str(ctx.message.author)
        embed=discord.Embed(title= user + "'s Roles" , color=0xe392fe)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        for role in activateRoles:
            c.execute(f"""SELECT {role}
                          FROM dodos
                          WHERE id = {ctx.message.author.id}
            """)
            roleCount = str(c.fetchone()[0]) + " Dodo " + role + " roles"
            embed.add_field(name=roleCount, value="Information about how many of this role you have", inline=False)
        await ctx.send(embed=embed)
    #Statements all work fine
    # @commands.command()
    # async def addme(self,ctx):
    #     c.execute(f"""INSERT INTO dodos(id,Red,Orange,Yellow,Green,Teal,Copyright,Bluev2,Blue,Purple,Purplev2,Pink,Pinkv2,money)
    #             VALUES ('{ctx.message.author.id}',0,0,0,0,0,0,0,0,0,0,0,0,0)

    #     """)
    #     conn.commit()
    #     await ctx.send("Added into database")
    #     c.execute(f"""SELECT *
    #             FROM dodos
    #             WHERE id = {ctx.message.author.id}
    #     """)
    #     print(c.fetchall())

    # @commands.command()
    # async def deleteme(self,ctx):
    #     c.execute(f"""DELETE from dodos 
    #             WHERE id='{ctx.message.author.id}'
    #     """)
    #     conn.commit()
    #     await ctx.send("Deleted user from database")
    #     c.execute(f"""SELECT *
    #             FROM dodos

    #     """)
    #     print(c.fetchall())

    # @commands.command()
    # async def updateme(self,ctx):
    #     c.execute(f"""UPDATE dodos 
    #                 SET Red = 929131
    #                 WHERE id='{ctx.message.author.id}'
    #             """)
    #     conn.commit()
    #     await ctx.send("Updated red role from database")
    #     c.execute(f"""SELECT *
    #             FROM dodos
    #     """)
    #     print(c.fetchall())
    
    # @commands.command()
    # async def lookme(self,ctx):
    #     c.execute(f"""SELECT *
    #                 FROM dodos
    #                 WHERE id='{ctx.message.author.id}'
    #             """)
    #     conn.commit()
    #     await ctx.send("Looked up from database")
    #     print(c.fetchall())


    @commands.command()
    async def roles(self,ctx):
        embed=discord.Embed(title="Collectable Roles List" , color=0xe392fe)
        embed.add_field(name="Dodo Red", value="Red colouring", inline=False)
        embed.add_field(name="Dodo Orange", value="Orange colouring", inline=False)
        embed.add_field(name="Dodo Yellow", value="Yellow colouring", inline=False)
        embed.add_field(name="Dodo Green", value="Green colouring", inline=False)
        embed.add_field(name="Dodo Teal", value="Teal colouring", inline=False)
        embed.add_field(name="Dodo Copyright", value="Some sort of blue", inline=False)
        embed.add_field(name="Dodo Cyan", value="Cyan colouring", inline=False)
        embed.add_field(name="Dodo Blue", value="Blue colouring", inline=False)
        embed.add_field(name="Dodo Grape", value="Grape colouring", inline=False)
        embed.add_field(name="Dodo Purple", value="Purple colouring", inline=False)
        embed.add_field(name="Dodo Rose", value="Rose colouring", inline=False)
        embed.add_field(name="Dodo Pink", value="Pink colouring", inline=False)
        embed.add_field(name="Dodo Salmon", value="Salmon colouring", inline=False)
        await ctx.send(embed=embed)

    # @commands.command()
    # async def admembers(self,ctx):
    #     admin = discord.utils.get(ctx.guild.roles, name = "Dodo Op")
    #     if (admin in ctx.message.author.roles):
    #         members = ctx.guild.members
    #         for member in members:
    #             c.execute(f"""INSERT INTO dodos 
    #                         VALUES ('{member.id}',0,0,0,0,0,0,0,0,0,0,0,0,0)
    #                         """)
    #             conn.commit()
    #             print(f"Adding {member} as {member.id}")
    #             for role in rolesList:
    #                 roleDiscord = discord.utils.get(ctx.guild.roles, name=role)
    #                 if (roleDiscord in member.roles):
    #                     role = role.split(" ")
    #                     c.execute(f"""UPDATE dodos
    #                             SET {role[1]} = {role.split()[1]} - 1
    #                             WHERE id = {ctx.message.author.id}

    #                         """)
    #     else:
    #         await ctx.send("Invalid permissions")

#setup
def setup(client):
    client.add_cog(Utilities(client))
