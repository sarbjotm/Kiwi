import nextcord
from nextcord.ext import commands
import os
import random
import asyncio
import mysql
from nextcord.utils import get
from myconstants import rolesList, activateRoles


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def trade(self, ctx, prefix, role, member: nextcord.Member, other_prefix, other_role):
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
                        role_assign = nextcord.utils.get(ctx.guild.roles, name=str(role_trading_for))
                        await ctx.message.author.add_roles(role_assign)
                        # Remove activated role and role colour if user does not have these roles anymore
                        if int(user_role_count) - 1 == 0:
                            role_remove = nextcord.utils.get(ctx.guild.roles, name=str(role))
                            if role_remove in ctx.message.author.roles:
                                await ctx.message.author.remove_roles(role_remove)

                            role_remove = nextcord.utils.get(ctx.guild.roles, name=str(role_trading))
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
                        role_assign = nextcord.utils.get(ctx.guild.roles, name=str(role_trading))
                        await member.add_roles(role_assign)
                        # Remove activated role and role colour if user does not have these roles anymore
                        if int(other_user_role_count) - 1 == 0:
                            role_remove = nextcord.utils.get(ctx.guild.roles, name=str(other_role))
                            if role_remove in member.roles:
                                await member.remove_roles(role_remove)

                            role_remove = nextcord.utils.get(ctx.guild.roles, name=str(role_trading_for))
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
    @commands.guild_only()
    async def collect(self, ctx):
        # await ctx.send("Command disabled while other commands are added/edited")
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        role_assign = random.choices(rolesList,
                                     weights=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                              1, 1])[0]
        print(role_assign)
        role = nextcord.utils.get(ctx.guild.roles, name=role_assign)
        await ctx.message.author.add_roles(role)
        await ctx.send(
            f'You have drawn the {role} role! To activate it use the ,activate {role} command. Your next chance to roll is in 12 hours')
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
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
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
    @commands.guild_only()
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
                    role_remove = nextcord.utils.get(ctx.guild.roles, name=r)
                    if role_remove in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role_remove)
                        break

                role_assign = nextcord.utils.get(ctx.guild.roles, name=role.split(" ")[1])
                await ctx.message.author.add_roles(role_assign)
                try:
                    await ctx.message.add_reaction("👍")
                except:
                    await ctx.send(
                        "Cannot react to your message since you have me blocked, but letting you know you have performed the command.")
            else:
                await ctx.send("You do not have that role.")
        c.close()
        db.close()

    @activate.error
    async def activate_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,activate Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using activate. {error}")

    @commands.command()
    @commands.guild_only()
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
                role = nextcord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.add_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")

        c.close()
        db.close()

    @show.error
    async def show_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,show Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using show. {error}")

    @commands.command()
    @commands.guild_only()
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
                role = nextcord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.add_roles(role)
        await kiwi_message.edit(content='Task Completed')
        c.close()
        db.close()

    @commands.command()
    @commands.guild_only()
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
                role = nextcord.utils.get(ctx.guild.roles, name=role)
                await ctx.message.author.remove_roles(role)
                await ctx.message.add_reaction("👍")
            else:
                await ctx.send("You do not have that role")

        c.close()
        db.close()

    @hide.error
    async def hide_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,hide Dodo Role**")
        await channel.send(f"{ctx.message.author} experienced a error using hide. {error}")

    @commands.command()
    @commands.guild_only()
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
            role_remove = nextcord.utils.get(ctx.guild.roles, name=role)
            if role_remove in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role_remove)

        await kiwi_message.edit(content='Task Completed')
        c.close()
        db.close()

    @commands.command()
    @commands.guild_only()
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

        embed = nextcord.Embed(title=user + "'s Roles", description=embed_description, color=0xe392fe)
        #embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        # embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
        c.close()
        db.close()

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        embed_description = ""
        for role in rolesList:
            embed_description = embed_description + role + "\n"
        embed = nextcord.Embed(title="Collectable Roles List", description=embed_description, color=0xe392fe)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def keep(self, ctx, number):

        if not number.isdigit():
            await ctx.send("Please enter a whole number for quantity.")
            return

        number = int(number)

        if number <= -1:
            await ctx.send("Enter a number that is greater to or equal to 0")
            return

        reply = await ctx.send("Working on it! Please wait")
        money_gained = 0
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        for role in activateRoles:
            while True:
                c.execute(f"""SELECT {role}
                                FROM dodos
                                WHERE id = {ctx.message.author.id}

                """)
                role_count = ''.join(map(str, c.fetchall()[0]))

                if int(role_count) == 0:
                    role_remove = nextcord.utils.get(ctx.guild.roles, name=role)
                    if role_remove in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role_remove)
                    role_remove = nextcord.utils.get(ctx.guild.roles, name=f"Dodo {role}")
                    if role_remove in ctx.message.author.roles:
                        await ctx.message.author.remove_roles(role_remove)

                if int(role_count) == number or int(role_count) < number:
                    break

                c.execute(f"""UPDATE dodos
                  SET {role} = {role} - 1
                  WHERE id = {ctx.message.author.id}
                      """)
                db.commit()
                money_gained = money_gained + random.randint(1, 1000)

        c.execute(f"""UPDATE dodos
                          SET money = money + {money_gained}
                          WHERE id = {ctx.message.author.id}
                              """)
        db.commit()

        c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
        money = ''.join(map(str, c.fetchall()[0]))
        money_symbol = nextcord.utils.get(ctx.message.guild.emojis, name='money')
        await reply.edit(content=f'Task Completed. You earned {money_gained}. Your new total is {money} {money_symbol}')
        c.close()
        db.close()

    @keep.error
    async def keep_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send(
            "Syntax for this command is: **,keep x** Where x is the number of roles you would like to keep from each role")
        await channel.send(f"{ctx.message.author} experienced a error using sell. {error}")

    @commands.command()
    @commands.guild_only()
    async def whois(self, ctx, *role):
        role = role.split()
        role_string = ""
        embed_description = ""
        embed_description2 = ""
        for i in range(0, len(role)):
            role_string = role_string + role[i][0].upper() + role[i][1:].lower() + " "
        role_string = role_string.strip()
        role_discord = nextcord.utils.get(ctx.guild.roles, name=role_string)
        for m in ctx.guild.members:
            print(m)
            print(role_discord in m.roles)
            if role_discord in m.roles:
                if len(embed_description) + len(str(m.nick)) + 1 <= 4098:
                    embed_description = embed_description + m.nick + "\n"
                else:
                    embed_description2 = embed_description2 + m.nick + "\n"

        embed = nextcord.Embed(title=f"Users who have the role {role_string} activated",
                              description=embed_description, color=0xe392fe)
        await ctx.send(embed=embed)
        print("WORKING")
        if len(str(embed_description2)) > 1:
            embed2 = nextcord.Embed(title=f"Users who have the role {role_string} activated continued",
                                   description=embed_description, color=0xe392fe)
            await ctx.send(embed=embed2)

    @whois.error
    async def whois_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Insert Generic message here")
        await channel.send(f"{ctx.message.author} experienced a error using whois. {error}")
        


# setup
def setup(client):
    client.add_cog(Utilities(client))
