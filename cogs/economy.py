import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path

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
        await ctx.send(f'You have {moneyAmount} {moneySymbol} ')
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
        amount = random.randint(1,1000);
        
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


def setup(client):
    client.add_cog(Economy(client))