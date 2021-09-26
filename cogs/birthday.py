from discord.ext import commands
import os
import mysql


# Mentions
class Birthday(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command(aliases=['birthday'])
    @commands.guild_only()
    async def setbirthday(self, ctx, mmdd):
        db = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
        c = db.cursor()
        date = str(mmdd)
        if len(date) != 3 or len(date) != 4:
            await ctx.send("Please enter your birthdate in the following way: mmdd")
        elif (int(date[0:2]) > 12) or (int(date[0:2]) < 1):
            await ctx.send("Not a valid month. Enter your birthdate in the following way: mmdd")
        elif (int(date[2:4]) > 31) or (int(date[2:4]) < 1):
            await ctx.send("Not a valid date. Enter your birthdate in the following way: mmdd")
        elif (int(date[0:2]) == 2) and (int(date[2:4]) > 29):
            await ctx.send("Feb does not have 30 or 31 days")
        elif (int(date[0:2]) == 4) and (int(date[2:4]) > 30):
            await ctx.send("April does not have 31 days")
        elif (int(date[0:2]) == 6) and (int(date[2:4]) > 30):
            await ctx.send("June does not have 31 days")
        elif (int(date[0:2]) == 9) and (int(date[2:4]) > 30):
            await ctx.send("Sept does not have 31 days")
        elif (int(date[0:2]) == 11) and (int(date[2:4]) > 30):
            await ctx.send("Nov does not have 31 days")
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
