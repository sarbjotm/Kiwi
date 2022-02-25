import nextcord
from nextcord.ext import commands
import os
import random
import mysql

from myconstants import rolesList, activateRoles


# Mentions
class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['balance'])
    @commands.guild_only()
    async def bal(self, ctx):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
        money_amount = ''.join(map(str, c.fetchall()[0]))
        money_symbol = nextcord.utils.get(ctx.message.guild.emojis, name='money')
        await ctx.send(f'You have {money_amount} {money_symbol}')
        c.close()
        db.close()

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.guild_only()
    async def daily(self, ctx):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        daily = ["Increase", "Decrease"]
        role_assign = random.choices(daily, weights=[9.5, 0.5])[0]  # 9.5 + 0.5 = 10; 0.5 / 10 -> 5% of stealing
        amount = random.randint(1, 1000)
        if role_assign == "Decrease":
            amount = amount * -1

        c.execute(f"""UPDATE dodos
                    SET money = money + {amount}
                    WHERE id = {ctx.message.author.id}
        """)
        db.commit()
        c.execute(f"""SELECT money
            FROM dodos
            WHERE id = {ctx.message.author.id}
        """)
        money_amount = ''.join(map(str, c.fetchall()[0]))
        money_symbol = nextcord.utils.get(ctx.message.guild.emojis, name='money')
        if amount < 0:
            await ctx.send(f"Oh no! Kiwi stole ${amount * -1}. Your new total is {money_amount} {money_symbol}")
        else:
            await ctx.send(f"You found ${amount}. Your new total is {money_amount} {money_symbol}")
        c.close()
        db.close()

    @daily.error
    async def daily_error(self, ctx, error):
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
            await channel.send(f"{ctx.message.author} experienced a cooldown error")

    @commands.command(aliases=['shopinfo'])
    @commands.guild_only()
    async def shop(self, ctx):
        embed = nextcord.Embed(title="Kiwi Shop", color=0xe392fe)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/6c/ce/3e/6cce3e4715c7886a4d599e3f029ef012.png")
        for i in range(0, len(rolesList)):
            embed.add_field(name=rolesList[i], value="3500 Dodo Dollars", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def sell(self, ctx, quantity, *role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        if not quantity.isdigit():
            await ctx.send("Please enter a whole number for quantity.")
        elif len(role) != 2:
            await ctx.send("Please enter a Dodo Role.")
        else:
            quantity = int(quantity)
            role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()

            if quantity <= 0:
                await ctx.send("Please enter a quantity greater than 0")

            elif role not in rolesList:
                await ctx.send("Please enter a Dodo Role. Example Usage ,sell  <amount> Dodo Red")
            else:
                total_profit = 0
                role = str(role)
                dodo_role = role
                role = role.split()[1]
                print("Saved role is: " + dodo_role)
                print("Database role role is: " + role)
                c.execute(f"""SELECT {role}
                                FROM dodos
                                WHERE id = {ctx.message.author.id}

                """)

                role_amount = ''.join(map(str, c.fetchall()[0]))
                role_amount = int(role_amount)

                if role_amount - quantity >= 0:
                    print("Role Amount is greater than 1")
                    c.execute(f"""UPDATE dodos
                    SET {role} = {role} - {quantity}
                    WHERE id = {ctx.message.author.id}
                        """)
                    db.commit()

                    for i in range(quantity):
                        sold_amount = random.randint(1, 1000)
                        total_profit = total_profit + sold_amount
                        c.execute(f"""UPDATE dodos
                        SET money = money + {sold_amount}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

                    """)
                    money_amount = ''.join(map(str, c.fetchall()[0]))
                    money_symbol = nextcord.utils.get(ctx.message.guild.emojis, name='money')
                    await ctx.send(f"You sold your role(s) for ${total_profit} {money_symbol}. Your new total is {money_amount} {money_symbol}")

                    c.execute(f"""SELECT {role}
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

                    """)
                    role_amount = ''.join(map(str, c.fetchall()[0]))

                    if int(role_amount) == 0:
                        role_remove = nextcord.utils.get(ctx.guild.roles, name=dodo_role)
                        if role_remove in ctx.message.author.roles:
                            await ctx.message.author.remove_roles(role_remove)
                        role_remove = nextcord.utils.get(ctx.guild.roles, name=role)
                        if role_remove in ctx.message.author.roles:
                            await ctx.message.author.remove_roles(role_remove)

                else:
                    await ctx.send("You do not have that many role(s)")

        c.close()
        db.close()

    @sell.error
    async def sell_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send(
            "Syntax for this command is: **,sell x Dodo Role** Where x is the number of roles you want to sell")
        await channel.send(f"{ctx.message.author} experienced a error using sell. {error}")

    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, quantity, *role):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        if not quantity.isdigit():
            await ctx.send("Please enter a whole number for **quantity**.")

        elif len(role) != 2:
            await ctx.send("Please enter a Dodo Role")

        else:
            quantity = int(quantity)
            role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()

            if quantity <= 0:
                await ctx.send("Please enter a quantity greater than 0")

            elif role not in rolesList:
                await ctx.send("Please enter a Dodo Role")

            else:
                bought_amount = 3500 * quantity
                role = str(role)
                dodo_role = role
                role = role.split(" ")[1]
                c.execute(f'''SELECT money 
                            FROM dodos
                            WHERE id = {ctx.message.author.id}
                
                ''')
                money_amount = ''.join(map(str, c.fetchall()[0]))
                if int(money_amount) < bought_amount:
                    await ctx.send(f"Sorry, but you cannot afford this role")
                else:
                    c.execute(f"""UPDATE dodos
                    SET money = money - {bought_amount}
                    WHERE id = {ctx.message.author.id}
                    """)
                    db.commit()
                    role_bought = nextcord.utils.get(ctx.guild.roles, name=dodo_role)
                    await ctx.message.author.add_roles(role_bought)
                    c.execute(f"""UPDATE dodos
                    SET {role} = {role} + {quantity}
                    WHERE id = {ctx.message.author.id}
                    """)
                    db.commit()
                    await ctx.message.add_reaction("👍")

        c.close()
        db.close()

    @buy.error
    async def buy_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send(
            "Syntax for this command is: **,buy x Dodo Role** Where x is the number of roles you want to buy")
        await channel.send(f"{ctx.message.author} experienced a error using buy. {error}")

    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        c.execute(f"""SELECT id, money
                FROM dodos
                ORDER BY money DESC LIMIT 5""")
        leaders = c.fetchall()
        description_embed = ""

        for i in range(0, 5):
            position = i + 1
            username = int(leaders[i][0])
            money = str(leaders[i][1])
            description_embed = description_embed + str(position) + ". " + "<@" + str(username) + ">" + " : " + str(money) + "\n"
        embed = nextcord.Embed(title="Richest Dodos", color=0xe392fe)
        embed.set_thumbnail(url="https://i.imgur.com/5wjePlr.png")
        embed.add_field(name="Top 5", value=description_embed, inline=True)
        await ctx.send(embed=embed)
        
        c.close()
        db.close()

    @commands.command()
    @commands.guild_only()
    async def give(self, ctx, member: nextcord.Member, money):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )

        c = db.cursor()
        c.execute(f"""SELECT money
            FROM dodos
            WHERE id = {ctx.message.author.id}


        """)
        money_amount = ''.join(map(str, c.fetchall()[0]))
        money_amount = int(money_amount)

        if member.id == ctx.message.author.id:
            await ctx.send("You can't give money to yourself")

        elif money_amount < int(money):
            await ctx.send("You do not have that much money to give out")

        elif int(money) <= 0:
            await ctx.send("You have to give at least 1 Dodo Dollar")

        else:
            c.execute(f"""UPDATE dodos
                    SET money = money - {money}
                    WHERE id = {ctx.message.author.id}
                    """)
            db.commit()

            c.execute(f"""UPDATE dodos
                    SET money = money + {money}
                    WHERE id = {member.id}
                    """)
            db.commit()

            await ctx.send("Transaction complete")

        c.close()
        db.close()

    @give.error
    async def give_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Syntax for this command is: **,give @User x** \
                       Where x is the dollar amount you would like to give to the user")
        await channel.send(f"{ctx.message.author} experienced a error using give. {error}")


def setup(client):
    client.add_cog(Economy(client))
