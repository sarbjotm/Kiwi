import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path

rolesList = ['Dodo Red','Dodo Orange','Dodo Yellow','Dodo Spring','Dodo Matcha' ,'Dodo Mint' , 'Dodo Green','Dodo Ice','Dodo Bbblu','Dodo Teal','Dodo Copyright','Dodo Cyan','Dodo Blue','Dodo Lavender','Dodo Grape','Dodo Purple','Dodo Rose','Dodo Pink','Dodo Salmon','Dodo Special']
activateRoles = ['Red','Orange','Yellow','Green','Teal','Copyright','Cyan','Blue','Grape','Purple','Rose','Pink','Salmon','Spring','Matcha','Mint','Ice','Bbblu','Lavender','Special']

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trade(self,ctx,role: discord.Role,member : discord.Member,roleOther: discord.Role):
        await ctx.send(f"Command under maintenace")
        # db = mysql.connector.connect(
        #     host= os.environ['HOST'],
        #     user = os.environ['USER'],
        #     password = os.environ['PASSWORD'],
        #     database = os.environ['DATABASE']
        # )
        # c = db.cursor()  
        # if ((str(role) not in rolesList) or (str(roleOther) not in rolesList)):
        #     await ctx.send("Trade only collectable roles")
        # elif ((role in ctx.message.author.roles) and (roleOther in member.roles)):  
        #     await ctx.send(f'{ctx.message.author.mention} wants to trade {role} to {member.mention} for {roleOther}')
        #     await ctx.send(f'{member.mention} do you accept? (Yes/No). You have 30 seconds to accept')
        #     try:
        #         msg = await self.client.wait_for(
        #             "message",
        #             timeout = 30,
        #             check=lambda message: message.author == member \
        #                 and message.channel == ctx.channel 
        #         )
        #         msg = msg.content.strip().lower()
        #         if msg == 'yes':
        #             await ctx.message.author.add_roles(roleOther) 
        #             #
        #             c.execute(f"""
        #                 UPDATE dodos
        #                 SET {str(roleOther).split(" ")[1]} = {str(roleOther).split(" ")[1]} + 1
        #                 WHERE id = {ctx.message.author.id}

                    
        #             """)
        #             db.commit()
        #             c.execute(f"""
        #                 UPDATE dodos
        #                 SET {str(role).split(" ")[1]} = {str(role).split(" ")[1]} - 1
        #                 WHERE id = {ctx.message.author.id}

                    
        #             """)
        #             db.commit()
        #             await member.add_roles(role) #Add role (Make SQL Here)
        #             #SQL
        #             c.execute(f"""
        #                 UPDATE dodos
        #                 SET {str(role).split(" ")[1]} = {str(role).split(" ")[1]} + 1
        #                 WHERE id = {member.id}

        #             """)
        #             db.commit()
        #             c.execute(f"""
        #                 UPDATE dodos
        #                 SET {str(roleOther).split(" ")[1]} = {str(roleOther).split(" ")[1]} - 1
        #                 WHERE id = {member.id}

        #             """)
        #             db.commit()
                    #SQL HERE CHECK IF == 1 THEN REMOVE
                    # c.execute(f"""
                    #     SELECT {str(role).split(" ")[1]}
                    #     FROM dodos
                    #     WHERE {ctx.message.author.id}
                    # """)
                    # roleCount = ''.join(map(str,c.fetchall()[0]))
                    # print(roleCount)
                    # print(f"{ctx.message.author} has {roleCount} {str(role)}") 

                    # if(int(roleCount) == 0):
                #     await ctx.message.author.remove_roles(role)
                #     # print(f"Removed role from {ctx.message.author}")
                    
                #     # c.execute(f"""
                #     #     SELECT {str(roleOther).split(" ")[1]}
                #     #     FROM dodos
                #     #     WHERE {member.id}
                    
                #     # """)
                #     # roleCount = ''.join(map(str,c.fetchall()[0]))
                #     # print(roleCount)
                #     # print(f"{member} has {roleCount} {str(roleOther)}")

                #     # if(int(roleCount) == 0):
                #     await member.remove_roles(roleOther)
                #     # print(f"Removed role from {member}")
                #     role = str(role)
                #     role = role.split(" ")[1]
                #     roleRemove = discord.utils.get(ctx.guild.roles, name=role)
                #     await ctx.message.author.remove_roles(roleRemove)
                #     roleOther = str(roleOther)
                #     roleOther = roleOther.split()[1]
                #     roleRemove = discord.utils.get(ctx.guild.roles, name=roleOther)
                #     await member.remove_roles(roleRemove) 

                #     #Add role if needed
                #     for role in activateRoles:
                #         c.execute(f"""SELECT {role.split(" ")[1]}
                #                     FROM dodos
                #                     WHERE id = {ctx.message.author.id}

                #     """)
                #         roleCount = c.fetchone()[0]
                #         if (roleCount > 0):
                #             roleAdd = discord.utils.get(ctx.guild.roles, name=role)
                #             print(f"Added {role} to {ctx.message.author}")
                #             await ctx.message.author.add_roles(roleAdd)

                #     for role in activateRoles:
                #         c.execute(f"""SELECT {role.split(" ")[1]}
                #                     FROM dodos
                #                     WHERE id = {member.id}

                #     """)
                #         roleCount = c.fetchone()[0]
                #         if (roleCount > 0):
                #             roleAdd = discord.utils.get(ctx.guild.roles, name=role)
                #             print(f"Added {role} to {member}")
                #             await member.add_roles(roleAdd)



                #     await ctx.send(f'Trade Completed!')
                # elif msg == 'no':
                #     await ctx.send(f'Trade Rejected!')
                # else:
                #     await ctx.send(f'Invalid input. Trade Rejected')
                # c.close()
                # db.close()

        #     except asyncio.TimeoutError:
        #         await ctx.send(f'Cancelling due to time out ') 
        # else:
        #     await ctx.send(f'You or the user you want to trade with does not have the role listed in the trade')   

    @commands.command()
    @commands.cooldown(1,43200, commands.BucketType.user)
    async def collect(self,ctx):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        roleAssign = random.choices(rolesList, weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])[0]
        print(roleAssign)
        role = discord.utils.get(ctx.guild.roles, name=roleAssign)
        await ctx.message.author.add_roles(role)
        await ctx.send(f'You have drawn the {role} role! To activate it use the ,activate {role} command. Your next chance to roll is in 12 hours')
        roleAssign = roleAssign.split(" ")
        c.execute(f"""UPDATE dodos
                    SET {roleAssign[1]} = {roleAssign[1]} + 1
                    WHERE id = {ctx.message.author.id}
        """)
        db.commit()

        c.execute(f"""SELECT {roleAssign[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
        """)
        roleCount = ''.join(map(str,c.fetchall()[0]))
        print(roleCount)
        await ctx.send(f'You now have {roleCount} {str(role)} roles')
        c.close()
        db.close()

    @collect.error
    async def collect_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            hours = int(seconds // 3600)
            seconds %= 3600
            minutes = int(seconds // 60)
            seconds %= 60
            seconds = int(seconds)
            if hours != 0:
                await ctx.send(f'Try again in {hours} hours {minutes} minutes and {seconds} seconds')
            else:
                await ctx.send(f'Try again in {minutes} minutes and {seconds} seconds')
            await channel.send(f"{ctx.message.author} experienced a cooldown error. {error}")


    @commands.command()
    async def activate(self,ctx,*role):
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = discord.utils.get(ctx.guild.roles, name = role)
        if ((str(role) not in rolesList)):
            await ctx.send("Only can activate collected Colour Roles.")
        elif (role in ctx.message.author.roles):
            for r in activateRoles:
                    roleRemove = discord.utils.get(ctx.guild.roles, name=r)
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                        break
            role = str(role)
            role = role.split()[1]
            roleAssign = discord.utils.get(ctx.guild.roles, name=role)
            await ctx.message.author.add_roles(roleAssign)
            await ctx.message.add_reaction("👍")
        
        else:
            await ctx.send("You do not have that role.")
        

    @commands.command()
    async def myroles(self,ctx):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        user = str(ctx.message.author)
        embed=discord.Embed(title= user + "'s Roles" , color=0xe392fe)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        for role in activateRoles:
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            description = "You have " + roleCount
            embed.add_field(name="Dodo " + role,value = description,inline=True)

        await ctx.send(embed=embed)
        c.close()
        db.close()

    @commands.command()
    async def roles(self,ctx):
        embed=discord.Embed(title="Collectable Roles List" , color=0xe392fe)
        embed.add_field(name="Dodo Red", value="Red colouring", inline=True)
        embed.add_field(name="Dodo Orange", value="Orange colouring", inline=True)
        embed.add_field(name="Dodo Yellow", value="Yellow colouring", inline=True)
        embed.add_field(name="Dodo Matcha", value="Matcha colouring", inline=True)
        embed.add_field(name="Dodo Spring", value="Spring colouring", inline=True)
        embed.add_field(name="Dodo Mint", value="Mint colouring", inline=True)
        embed.add_field(name="Dodo Green", value="Green colouring", inline=True)
        embed.add_field(name="Dodo Teal", value="Teal colouring", inline=True)
        embed.add_field(name="Dodo Copyright", value="Tiffany Blue colouring", inline=True)
        embed.add_field(name="Dodo Cyan", value="Cyan colouring", inline=True)
        embed.add_field(name="Dodo Blue", value="Blue colouring", inline=True)
        embed.add_field(name="Dodo Bbblu", value="Baby Blue colouring", inline=True)
        embed.add_field(name="Dodo Ice", value="Ice Cold colouring", inline=True)
        embed.add_field(name="Dodo Grape", value="Grape colouring", inline=True)
        embed.add_field(name="Dodo Purple", value="Purple colouring", inline=True)
        embed.add_field(name="Dodo Lavender", value="Lavender colouring", inline=True)
        embed.add_field(name="Dodo Rose", value="Rose colouring", inline=True)
        embed.add_field(name="Dodo Pink", value="Pink colouring", inline=True)
        embed.add_field(name="Dodo Salmon", value="Salmon colouring", inline=True)
        embed.add_field(name="Dodo Special", value="Look at the hex code", inline=True)
        await ctx.send(embed=embed)


#setup
def setup(client):
    client.add_cog(Utilities(client))
