import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path


rolesList = ['Dodo Red','Dodo Orange','Dodo Yellow','Dodo Spring','Dodo Matcha' ,'Dodo Mint' , 'Dodo Green','Dodo Ice','Dodo Bbblu','Dodo Teal','Dodo Copyright','Dodo Cyan','Dodo Blue','Dodo Lavender','Dodo Grape','Dodo Purple','Dodo Rose','Dodo Pink','Dodo Salmon','Dodo Special']

#Mentions
class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['balance'])
    async def bal(self,ctx):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor()
        c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

        """)
        moneyAmount = ''.join(map(str,c.fetchall()[0]))
        moneySymbol = discord.utils.get(ctx.message.guild.emojis, name='money')
        await ctx.send(f'You have {moneyAmount} {moneySymbol}')
        c.close()
        db.close() 

    @commands.command()
    @commands.cooldown(1,86400, commands.BucketType.user)
    async def daily(self,ctx):   
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor() 
        daily = ["Increase", "Decrease"]
        roleAssign = random.choices(daily, weights = [9.5,0.5])[0]
        amount = random.randint(1,1000);
        if (roleAssign == "Decrease"):
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
        moneyAmount = ''.join(map(str,c.fetchall()[0]))
        moneySymbol = discord.utils.get(ctx.message.guild.emojis, name='money')
        if(amount < 0):
            await ctx.send(f"Oh no! Kiwi stole ${amount*-1}. Your new total is {moneyAmount} {moneySymbol}")
        else:
            await ctx.send(f"You found ${amount}. Your new total is {moneyAmount} {moneySymbol}")
        c.close()
        db.close()
    
    @daily.error
    async def daily_error(self,ctx,error):
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
            
    @commands.command(aliases = ['shopinfo'])
    async def shop(self,ctx):
        embed=discord.Embed(title="Kiwi Shop" , color=0xe392fe)
        embed.set_thumbnail(url= "https://i.pinimg.com/originals/6c/ce/3e/6cce3e4715c7886a4d599e3f029ef012.png")
        for i in range(0,len(rolesList)):
            embed.add_field(name=rolesList[i], value="5000 Dodo Dollars", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def sell(self,ctx, quantity, *role):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        quantity = int(quantity)
        if(len(role) != 2):
            await ctx.send("Please enter a Dodo Role. Example Usage ,sell Dodo Red")
        
        else:
            role = role[0][0].upper() + role[0][1:].lower() + " " + role[1][0].upper() + role[1][1:].lower()

            if(quantity < 0):
                await ctx.send("Please enter a quantity greater than 0")
        
            elif( (role not in rolesList) ):
                await ctx.send("Please enter a Dodo Role. Example Usage ,sell Dodo Red")
            else:
                totalProfit = 0
                soldAmount = 0
                c = db.cursor()
                role = str(role)
                dodoRole = role
                role = role.split()[1]
                print("Saved role is: " + dodoRole)
                print("Database role role is: " + role)
                c.execute(f"""SELECT {role}
                                FROM dodos
                                WHERE id = {ctx.message.author.id}

                """)


                roleAmount = ''.join(map(str,c.fetchall()[0]))
                roleAmount = int(roleAmount)
                
                
                if(roleAmount-quantity >= 1):
                    print("Role Amount is greater than 1")
                    c.execute(f"""UPDATE dodos
                    SET {role} = {role} - {quantity}
                    WHERE id = {ctx.message.author.id}
                        """)
                    db.commit()

                    for i in range(quantity):
                        soldAmount = random.randint(1,750)
                        totalProfit = totalProfit + soldAmount
                        c.execute(f"""UPDATE dodos
                        SET money = money + {soldAmount}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}


                    """)
                    moneyAmount = ''.join(map(str,c.fetchall()[0]))
                    moneySymbol = discord.utils.get(ctx.message.guild.emojis, name='money')
                    await ctx.send(f"You sold your role(s) for ${totalProfit} {moneySymbol}. Your new total is {moneyAmount} {moneySymbol}")

                elif(roleAmount-quantity == 0):
                    c.execute(f"""UPDATE dodos
                    SET {role} = {role} - {quantity}
                    WHERE id = {ctx.message.author.id}
                        """)
                    db.commit()
                    roleRemove = discord.utils.get(ctx.guild.roles, name=dodoRole)
                    await ctx.message.author.remove_roles(roleRemove)
                    roleRemove = discord.utils.get(ctx.guild.roles, name=role)
                    if(roleRemove in ctx.message.author.roles):
                        await ctx.message.author.remove_roles(roleRemove)
                    
                    for i in range(quantity):
                        soldAmount = random.randint(1,750)
                        totalProfit = totalProfit + soldAmount
                        c.execute(f"""UPDATE dodos
                        SET money = money + {soldAmount}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
    
                    
                    c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}


                    """)
                    moneyAmount = ''.join(map(str,c.fetchall()[0]))
                    moneySymbol = discord.utils.get(ctx.message.guild.emojis, name='money')
                    await ctx.send(f"You sold your role(s) for ${totalProfit} {moneySymbol}. Your new total is {moneyAmount} {moneySymbol}")

                else:
                    print("Role Amount is equal to 0")
                    await ctx.send("You do not have that many role(s)")

        c.close()
        db.close()

    @commands.command()

    async def leaderboard(self,ctx):
        db = mysql.connector.connect(
        host= os.environ['HOST'],
        user = os.environ['USER'],
        password = os.environ['PASSWORD'],
        database = os.environ['DATABASE']
        )
        c = db.cursor()  
        c.execute(f"""SELECT id, money
                FROM dodos
                ORDER BY money DESC LIMIT 5""") 
        leaders = c.fetchall()
        # print(leaders)
        # print(leaders[0][0])
        # print(leaders[0][1])
        # embed=discord.Embed(title="Top 5 Richest Dodos" , color=0xe392fe)
        descriptionEmbed = " "
        for i in range(0,5):
            position = i + 1
            username = await ctx.message.channel.guild.fetch_member(int(leaders[i][0]))
            money = leaders[i][1]
            descriptionEmbed = descriptionEmbed + position + ". " + username + "-" + money + "\n" 
        embed=discord.Embed(title="Richest Dodos" , color=0xe392fe)
        embed.set_thumbnail(url= "https://i.imgur.com/5wjePlr.png")
        embed.add_field(name="Top 5", value = descriptionEmbed, inline=True)
        await ctx.send(embed=embed)

            
        c.close()
        db.close()
        await ctx.send("TODO: FINISH THIS")



def setup(client):
    client.add_cog(Economy(client))