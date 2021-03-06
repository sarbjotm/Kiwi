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
    async def trade(self,ctx,*arguments):
        await ctx.send(f"Command under maintenace")
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor()
        if len(arguments != 5):
            await ctx.send("Error in arguments. Example usage is as follows ,trade Dodo Red @User Dodo Blue")
        userRoleString = arguments[0][0].upper() + arguments[0][1:].lower() + " " + arguments[1][0].upper() + arguments[1][1:].lower()
        otherUserID = arguments[2][3:len(arguments[2])-1]
        otherUserRoleString = arguments[3][0].upper() + arguments[0][1:].lower() + " " + arguments[4][0].upper() + arguments[1][1:].lower()
        
        if( (userRoleString in rolesList) and (otherUserRoleString in rolesList)):
        #Grab user role count
            c.execute(f"""SELECT {userRoleString[1]}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}        
            """)
            userRoleCount = ''.join(map(str,c.fetchall()[0]))

            #Grab other user role count
            c.execute(f"""SELECT {otherUserRoleString[1]}
                        FROM dodos
                        WHERE id = {otherUserRoleString}        
            """)
            otherUserRoleCount = ''.join(map(str,c.fetchall()[0]))
            if( (userRoleCount > 0) and (otherUserRoleCount > 0) ):
                #Update USER Info and Remove roles if needed

                c.execute(f"""UPDATE dodos
                              SET{userRoleString.split(" ")[1]} = {userRoleString.split(" ")[1]} - 1
                              WHERE id = {ctx.message.author.id}
                
                """)
                db.commit()
                c.execute(f"""UPDATE dodos
                        SET{otherUserRoleString.split(" ")[1]} = {otherUserRoleString.split(" ")[1]} + 1
                        WHERE id = {ctx.message.author.id}

                """)
                db.commit()


                role = discord.utils.get(ctx.guild.roles, name=otherUserRoleString)
                await ctx.message.author.add_roles(role)


                if(userRoleCount - 1 == 0):
                    roleRemove = discord.utils.get(ctx.guild.roles, name=userRoleString.split(" ")[1])
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                    roleRemove = discord.utils.get(ctx.guild.roles, name=userRoleString)
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                

                #Update OTHER user Info
                c.execute(f"""UPDATE dodos
                              SET{otherUserRoleString.split(" ")[1]} = {otherUserRoleString.split(" ")[1]} - 1
                              WHERE id = {otherUserID}
                
                """)
                db.commit()
                c.execute(f"""UPDATE dodos
                        SET{userRoleString.split(" ")[1]} = {userRoleString.split(" ")[1]} + 1
                        WHERE id = {otherUserID}

                """)
                db.commit()

                role = discord.utils.get(ctx.guild.roles, name=userRoleString)
                await ctx.guild.get_member(int(otherUserID)).add_roles(role)

                if(otherUserRoleCount - 1 == 0):
                    roleRemove = discord.utils.get(ctx.guild.roles, name=otherUserRoleString.split(" ")[1])
                    if(roleRemove in ctx.guild.get_member(int(otherUserID))):
                        await ctx.guild.get_member(int(otherUserID)).remove_roles(roleRemove)
                    roleRemove = discord.utils.get(ctx.guild.roles, name=otherUserRoleString)
                    if(roleRemove in ctx.guild.get_member(int(otherUserID))):
                        await ctx.guild.get_member(int(otherUserID)).remove_roles(roleRemove)
                    
                            
                await ctx.send("Trade Complete!")


            else:
                await ctx.send("Users do not have those roles or they do not exist")
        else:
            await ctx.send("You can only trade collectable Dodo Roles")
    @commands.command()
    async def amandertesting(self,ctx,*arguments):
        await ctx.send(arguments)
        print(arguments[2])
        print(arguments[2][3:len(arguments[2])-1])

    @commands.command()
    @commands.cooldown(1,43200, commands.BucketType.user)
    async def collect(self,ctx):
        await ctx.send("Command disabled while other commands are added/edited")
        # db = mysql.connector.connect(
        #     host= os.environ['HOST'],
        #     user = os.environ['USER'],
        #     password = os.environ['PASSWORD'],
        #     database = os.environ['DATABASE']
        # )
        # c = db.cursor() 
        # roleAssign = random.choices(rolesList, weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])[0]
        # print(roleAssign)
        # role = discord.utils.get(ctx.guild.roles, name=roleAssign)
        # await ctx.message.author.add_roles(role)
        # await ctx.send(f'You have drawn the {role} role! To activate it use the ,activate {role} command. Your next chance to roll is in 12 hours')
        # roleAssign = roleAssign.split(" ")
        # c.execute(f"""UPDATE dodos
        #             SET {roleAssign[1]} = {roleAssign[1]} + 1
        #             WHERE id = {ctx.message.author.id}
        # """)
        # db.commit()

        # c.execute(f"""SELECT {roleAssign[1]}
        #             FROM dodos
        #             WHERE id = {ctx.message.author.id}
    
    
        # """)
        # roleCount = ''.join(map(str,c.fetchall()[0]))
        # print(roleCount)
        # await ctx.send(f'You now have {roleCount} {str(role)} roles')
        # c.close()
        # db.close()

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
            description = roleCount + " Dodo " + role  + " roles"
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
