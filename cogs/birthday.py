import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path



#Mentions
class Birthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['birthday'])
    async def setbirthday(self,ctx, mmdd):
        db = mysql.connector.connect(
            host= os.environ['HOST'],
            user = os.environ['USER'],
            password = os.environ['PASSWORD'],
            database = os.environ['DATABASE']
        )
        c = db.cursor()
        date = str(mmdd)
        if(len(date) != 4):
            await ctx.send("Please enter your birthdate in the following way: mmdd")
        elif ((int(date[0:2]) > 12) or (int(date[0:2]) < 1) ):
            await ctx.send("Not a valid month. Enter your birthdate in the following way: mmdd")
        elif ((int(date[2:4]) > 31) or (int(date[2:4]) < 1) ):
            await ctx.send("Not a valid date. Enter your birthdate in the following way: mmdd")
        elif ((int(date[0:2]) == 2) and (int(date[2:4]) > 29) ):
            await ctx.send("Feb does not have 30 or 31 days")
        elif( ( (int(date[0:2] == 4)) or (int(date[0:2] == 6)) or (int(date[0:2] == 9)) or (int(date[0:2] == 11)) ) and (int(date[2:4] == 31)) ):
            await ctx.send("That month has 30 days only, not 31 days. enter your birthdate in the following way: mmdd")
        else:
            c.execute(f"""UPDATE dodos
            SET birthday = {date}
            WHERE id = {ctx.message.author.id}

        """)
            db.commit()
            await ctx.send(f"Added {date} as your birthday. Will wish you a happy birthday then!")
        c.close()
        db.close()
        





def setup(client):
    client.add_cog(Birthday(client))