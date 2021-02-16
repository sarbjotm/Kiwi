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
        roleAssign = random.choices(daily, weights = [3,1])[0]
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
            await ctx.send(f"Oh no! Kiwi stole ${amount}. Your new total is {moneyAmount} {moneySymbol}")
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
        moneySymbol = discord.utils.get(ctx.message.guild.emojis, name='money')
        descriptionEmbed = " "
        for i in range(0,len(rolesList)):
            descriptionEmbed = descriptionEmbed + rolesList[i] + "- Price: 5000 " + moneySymbol + "\n" 

        embed=discord.Embed(title="Kiwi Shop" , color=0xe392fe)
        embed.set_thumbnail(url= "https://sdl-stickershop.line.naver.jp/products/0/0/1/1233993/android/stickers/9496426.png;compress=true")
        embed.add_field(name="Items to Buy", value = descriptionEmbed, inline=True)
        await ctx.message.delete(delay = 0)
        sent = await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Economy(client))