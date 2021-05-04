import discord
from discord.ext import commands
import os
import random
import asyncio
import mysql

rolesList = ['Dodo Red', 'Dodo Orange', 'Dodo Yellow', 'Dodo Spring', 'Dodo Matcha', 'Dodo Mint', 'Dodo Green',
             'Dodo Ice', 'Dodo Bbblu', 'Dodo Teal', 'Dodo Copyright', 'Dodo Cyan', 'Dodo Blue', 'Dodo Lavender',
             'Dodo Grape', 'Dodo Purple', 'Dodo Rose', 'Dodo Pink', 'Dodo Salmon', 'Dodo Special', 'Dodo Taffy',
             'Dodo Oak', 'Dodo Snow', 'Dodo Black', 'Dodo Gold']
activateRoles = ['Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Copyright', 'Cyan', 'Blue', 'Grape', 'Purple', 'Rose',
                 'Pink', 'Salmon', 'Spring', 'Matcha', 'Mint', 'Ice', 'Bbblu', 'Lavender', 'Special', 'Taffy', 'Oak',
                 'Snow', 'Black', 'Gold']


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trade(self, ctx, prefix, role, member: discord.Member, other_prefix, other_role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )

        c = db.cursor()
        # Convert roles to Dodo Colour format
        role_trading = str(prefix[0].upper()) + str(prefix[1:].lower()) + " " + str(role[0].upper()) + str(
            role[1:].lower())
        role_trading_for = str(other_prefix[0].upper()) + str(other_prefix[1:].lower()) + " " + str(
            other_role[0].upper()) + str(other_role[1:].lower())
        if (str(role_trading) not in rolesList) or (str(role_trading_for) not in rolesList):
            await ctx.send("You can only trade collectable roles, here is an example: ,trade Dodo Red @User Dodo Blue")

        elif member.id == ctx.message.author.id:
            await ctx.send("You cannot trade with yourself")

        else:
            # Check if users have the roles in the database
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}
            
            """)
            user_role_count = ''.join(map(str, c.fetchall()[0]))

            c.execute(f"""SELECT {other_role}
                        FROM dodos
                        WHERE id = {member.id}
            
            """)
            other_user_role_count = ''.join(map(str, c.fetchall()[0]))

            if (int(user_role_count) == 0) or (int(other_user_role_count) == 0):
                await ctx.send("You or the user you're trading with does not have those roles")

            else:
                # Confirmation from other user that they accept the trade
                await ctx.send(
                    f'{ctx.message.author.mention} wants to trade {role_trading} to {member.mention} for {role_trading_for}')
                await ctx.send(f'{member.mention} do you accept? (Yes/No). You have 30 seconds to accept')
                try:
                    msg = await self.client.wait_for(
                        "message",
                        timeout=30,
                        check=lambda message: message.author == member and message.channel == ctx.channel
                    )
                    # Update user who intiated trade
                    msg = msg.content.strip().lower()
                    if (msg == 'yes') or (msg == 'y'):
                        c.execute(f"""UPDATE dodos
                                    SET {role} = {role} - 1
                                    WHERE id = {ctx.message.author.id}
                        
                                """)
                        db.commit()
                        c.execute(f"""UPDATE dodos
                                    SET {other_role} = {other_role} + 1
                                    WHERE id = {ctx.message.author.id}
                        
                                """)
                        db.commit()
                        role_assign = discord.utils.get(ctx.guild.roles, name=str(role_trading_for))
                        await ctx.message.author.add_roles(role_assign)
                        # Remove activated role and role colour if user does not have these roles anymore
                        if int(user_role_count) - 1 == 0:
                            role_remove = discord.utils.get(ctx.guild.roles, name=str(role))
                            if role_remove in ctx.message.author.roles:
                                await ctx.message.author.remove_roles(role_remove)

                            role_remove = discord.utils.get(ctx.guild.roles, name=str(role_trading))
                            if role_remove in ctx.message.author.roles:
                                await ctx.message.author.remove_roles(role_remove)

                        # Other User Updating
                        c.execute(f"""UPDATE dodos
                                    SET {other_role} = {other_role} - 1
                                    WHERE id = {member.id}
                        
                                """)
                        db.commit()
                        c.execute(f"""UPDATE dodos
                                    SET {role} = {role} + 1
                                    WHERE id = {member.id}
                        
                                """)
                        db.commit()
                        role_assign = discord.utils.get(ctx.guild.roles, name=str(role_trading))
                        await member.add_roles(role_assign)
                        # Remove activated role and role colour if user does not have these roles anymore
                        if int(other_user_role_count) - 1 == 0:
                            role_remove = discord.utils.get(ctx.guild.roles, name=str(other_role))
                            if role_remove in member.roles:
                                await member.remove_roles(role_remove)

                            role_remove = discord.utils.get(ctx.guild.roles, name=str(role_trading_for))
                            if role_remove in member.roles:
                                await member.remove_roles(role_remove)

                        await ctx.send("Trade Complete!")
                    else:
                        await ctx.send(f'Trade Rejected')

                except asyncio.TimeoutError:
                    await ctx.send(f'Cancelling due to time out ')

        c.close()
        db.close()

    @trade.error
    async def trade_error(self, ctx, error):
        await ctx.send("Error Occurred. Syntax for this command is: **,trade Dodo Role @User Dodo Role**")

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def collect(self, ctx):
        # await ctx.send("Command disabled while other commands are added/edited")
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        role_assign = random.choices(rolesList, weights=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1])[0]
        print(role_assign)
        role = discord.utils.get(ctx.guild.roles, name=role_assign)
        await ctx.message.author.add_roles(role)
        await ctx.send(f'You have drawn the {role} role! To activate it use the ,activate {role} command. Your next chance to roll is in 12 hours')
        role_assign = role_assign.split(" ")
        c.execute(f"""UPDATE dodos
                    SET {role_assign[1]} = {role_assign[1]} + 1
                    WHERE id = {ctx.message.author.id}
        """)
        db.commit()

        c.execute(f"""SELECT {role_assign[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
        """)
        role_count = ''.join(map(str, c.fetchall()[0]))
        print(role_count)
        await ctx.send(f'You now have {role_count} {str(role)} roles')
        c.close()
        db.close()

    @collect.error
    async def collect_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
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
    async def activate(self, ctx, *role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        if role not in rolesList:
            await ctx.send("Only can activate collected Colour Roles.")
        else:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
            """)
            role_count = ''.join(map(str, c.fetchall()[0]))

            if int(role_count) > 0:
                for r in activateRoles:
                    role_remove = discord.utils.get(ctx.guild.roles, name=r)
                    if role_remove in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role_remove)
                        break

                role_assign = discord.utils.get(ctx.guild.roles, name=role.split(" ")[1])
                await ctx.message.author.add_roles(role_assign)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role.")
        c.close()
        db.close()

    @activate.error
    async def activate_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Error Occurred. Syntax for this command is: **,activate Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using activate. {error}")

    @commands.command()
    async def show(self, ctx, *role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        print(role)
        print(role.split())
        if role not in rolesList:
            await ctx.send("Only can show collectable roles")
        else:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            role_count = ''.join(map(str, c.fetchall()[0]))
            if int(role_count) > 0:
                role = discord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.add_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")

        c.close()
        db.close()

    @show.error
    async def show_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Error Occurred. Syntax for this command is: **,show Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using show. {error}")

    @commands.command()
    async def showall(self, ctx):
        kiwi_message = await ctx.send("Hacking in... please wait, will reply when finished")
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        for role in rolesList:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            role_count = ''.join(map(str, c.fetchall()[0]))
            if int(role_count) > 0:
                role = discord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.add_roles(role)
        await kiwi_message.edit(content='Task Completed')
        c.close()
        db.close()

    @commands.command()
    async def hide(self, ctx, *role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()
        role = str(role)
        if role not in rolesList:
            await ctx.send("Only can hide collectable roles")
        else:
            c.execute(f"""SELECT {role.split()[1]}
                    FROM dodos
                    WHERE id = {ctx.message.author.id}
    
    
            """)
            role_count = ''.join(map(str, c.fetchall()[0]))
            if int(role_count) > 0:
                role = discord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.remove_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")

        c.close()
        db.close()

    @hide.error
    async def hide_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Error Occurred. Syntax for this command is: **,hide Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using hide. {error}")

    @commands.command()
    async def hideall(self, ctx):
        kiwi_message = await ctx.send("Hacking in... please wait, will reply when finished")
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        for role in rolesList:
            role_remove = discord.utils.get(ctx.guild.roles, name=role)
            if role_remove in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role_remove)

        await kiwi_message.edit(content='Task Completed')
        c.close()
        db.close()

    @commands.command()
    async def myroles(self, ctx):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        embed_description = ""
        user = str(ctx.message.author)

        for role in activateRoles:
            c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
            role_count = ''.join(map(str, c.fetchall()[0]))
            embed_description = embed_description + role_count + " Dodo " + role + " roles" + "\n"

        embed = discord.Embed(title=user + "'s Roles", description=embed_description, color=0xe392fe)
        embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        # embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
        c.close()
        db.close()

    @commands.command()
    async def roles(self, ctx):
        embed_description = ""
        for role in rolesList:
            embed_description = embed_description + role + "\n"
        embed = discord.Embed(title="Collectable Roles List", description=embed_description, color=0xe392fe)
        await ctx.send(embed=embed)


# setup
def setup(client):
    client.add_cog(Utilities(client))
