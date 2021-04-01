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
    async def trade(self,ctx,prefix,role, member : discord.Member,otherPrefix, otherRole):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )

        c = db.cursor()
        #Convert roles to Dodo Colour format  
        roleTrading = str(prefix[0].upper()) + str(prefix[1:].lower())  + " " + str(role[0].upper()) + str(role[1:].lower())
        roleTradingFor = str(otherPrefix[0].upper()) + str(otherPrefix[1:].lower())  + " " + str(otherRole[0].upper()) + str(otherRole[1:].lower())
        if((str(roleTrading) not in rolesList) or (str(roleTradingFor) not in rolesList)):
            await ctx.send("You can only trade collectable roles, here is an example: ,trade Dodo Red @User Dodo Blue")
        
        elif(member.id == ctx.message.author.id):
            await ctx.send("You cannot trade with yourself")
        
        else:
            #Check if users have the roles in the database
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}
            
            """)
            userRoleCount = ''.join(map(str,c.fetchall()[0]))


            c.execute(f"""SELECT {otherRole}
                        FROM dodos
                        WHERE id = {member.id}
            
            """)
            otherUserRoleCount = ''.join(map(str,c.fetchall()[0]))

            if((int(userRoleCount) == 0) or (int(otherUserRoleCount) == 0)):
                await ctx.send("You or the user you're trading with does not have those roles")

            else:
                #Confirmation from other user that they accept the trade
                await ctx.send(f'{ctx.message.author.mention} wants to trade {roleTrading} to {member.mention} for {roleTradingFor}')
                await ctx.send(f'{member.mention} do you accept? (Yes/No). You have 30 seconds to accept')
                try:
                    msg = await self.client.wait_for(
                        "message",
                        timeout = 30,
                        check=lambda message: message.author == member \
                            and message.channel == ctx.channel 
                    )
                    #Update user who intiated trade
                    msg = msg.content.strip().lower()
                    if ( (msg == 'yes') or (msg == 'y')):
                        c.execute(f"""UPDATE dodos
                                    SET {role} = {role} - 1
                                    WHERE id = {ctx.message.author.id}
                        
                                """)
                        db.commit()
                        c.execute(f"""UPDATE dodos
                                    SET {otherRole} = {otherRole} + 1
                                    WHERE id = {ctx.message.author.id}
                        
                                """)
                        db.commit()
                        roleAssign = discord.utils.get(ctx.guild.roles, name=str(roleTradingFor))
                        await ctx.message.author.add_roles(roleAssign)
                        #Remove activated role and role colour if user does not have these roles anymore
                        if( int(userRoleCount) - 1 == 0):
                            roleRemove = discord.utils.get(ctx.guild.roles, name=str(role))
                            if(roleRemove in ctx.message.author.roles):
                                await ctx.message.author.remove_roles(roleRemove)

                            roleRemove = discord.utils.get(ctx.guild.roles, name= str(roleTrading))
                            if(roleRemove in ctx.message.author.roles):
                                await ctx.message.author.remove_roles(roleRemove)

                        #Other User Updating
                        c.execute(f"""UPDATE dodos
                                    SET {otherRole} = {otherRole} - 1
                                    WHERE id = {member.id}
                        
                                """)
                        db.commit()
                        c.execute(f"""UPDATE dodos
                                    SET {role} = {role} + 1
                                    WHERE id = {member.id}
                        
                                """)
                        db.commit()
                        roleAssign = discord.utils.get(ctx.guild.roles, name=str(roleTrading))
                        await member.add_roles(roleAssign)
                        #Remove activated role and role colour if user does not have these roles anymore
                        if(int(otherUserRoleCount) - 1 == 0):
                            roleRemove = discord.utils.get(ctx.guild.roles, name=str(otherRole))
                            if(roleRemove in member.roles):
                                await member.remove_roles(roleRemove)

                            roleRemove = discord.utils.get(ctx.guild.roles, name= str(roleTradingFor))
                            if(roleRemove in member.roles):
                                await member.remove_roles(roleRemove)
                        
                        await ctx.send("Trade Complete!")
                    else:
                        await ctx.send(f'Trade Rejected')

                except asyncio.TimeoutError:
                    await ctx.send(f'Cancelling due to time out ') 

        c.close()
        db.close()

    @trade.error
    async def trade_error(self,ctx,error):
        await ctx.send("Error Occured. Syntax for this command is: **,trade Dodo Role @User Dodo Role**")

    @commands.command()
    @commands.cooldown(1,43200, commands.BucketType.user)
    async def collect(self,ctx):
        # await ctx.send("Command disabled while other commands are added/edited")
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        #roleAssign = random.choices(rolesList, weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])[0]
        roleAssign = rolesList[0]
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
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        if(role not in rolesList):
            await ctx.send("Only can activate collected Colour Roles.")
        else:
            role = random.choices(rolesList, weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])[0] #Remove after April 1
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
            """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            if(int(roleCount) > 0):
                for r in activateRoles:
                    roleRemove = discord.utils.get(ctx.guild.roles, name=r)
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                        break
                
                roleAssign = discord.utils.get(ctx.guild.roles, name=role.split(" ")[1])
                await ctx.message.author.add_roles(roleAssign)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role.")
        c.close()
        db.close()
    
    @activate.error
    async def activate_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,activate Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using activate")    
    
    @commands.command()
    async def show(self,ctx,*role):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        print(role)
        print(role.split())
        if((role not in rolesList)):
            await ctx.send("Only can show collecatable roles")
        else:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            if(int(roleCount) > 0):
                role = discord.utils.get(ctx.guild.roles, name = role)
                await ctx.message.author.add_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")
        
        c.close()
        db.close()

    @show.error
    async def show_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,show Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using show")    


    @commands.command()
    async def showall(self,ctx):
        kiwimessage = await ctx.send("Hacking in... please wait, will reply when finished")
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        for role in rolesList:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            if(int(roleCount) > 0):
                role = discord.utils.get(ctx.guild.roles, name = role)
                await ctx.message.author.add_roles(role)
        await kiwimessage.edit(content = 'Task Completed')        
        c.close()
        db.close()

    @commands.command()
    async def hide(self,ctx,*role):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        if((role not in rolesList)):
            await ctx.send("Only can hide collecatable roles")
        else:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            if(int(roleCount) > 0):
                role = discord.utils.get(ctx.guild.roles, name = role)
                await ctx.message.author.remove_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")
        
        c.close()
        db.close()
    
    @hide.error
    async def hide_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,hide Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using hide")  

    @commands.command()
    async def hideall(self,ctx):
        kiwimessage = await ctx.send("Hacking in... please wait, will reply when finished")
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        for role in rolesList:
            roleRemove = discord.utils.get(ctx.guild.roles, name=role)
            if(roleRemove in ctx.message.author.roles):
                await ctx.message.author.remove_roles(roleRemove)
                    
        await kiwimessage.edit(content = 'Task Completed')        
        c.close()
        db.close()


        

    @commands.command()
    async def myroles(self,ctx):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        embedDescription = ""
        user = str(ctx.message.author)
        
        for role in activateRoles:
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
            roleCount = ''.join(map(str,c.fetchall()[0]))
            embedDescription = embedDescription + roleCount + " Dodo " + role  + " roles" + "\n"

        embed=discord.Embed(title= user + "'s Roles", description = embedDescription, color=0xe392fe)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
        c.close()
        db.close()

    @commands.command()
    async def roles(self,ctx):
        embedDescription = ""
        for role in rolesList:
            embedDescription = embedDescription + role + "\n"
        embed=discord.Embed(title="Collectable Roles List", description = embedDescription, color=0xe392fe)
        await ctx.send(embed=embed)


#setup
def setup(client):
    client.add_cog(Utilities(client))
