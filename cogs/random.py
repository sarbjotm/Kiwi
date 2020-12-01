import discord
from discord.ext import commands
import random

#Chances
class Randomness(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command(aliases = ['rand'])
    async def randomnumber(self,ctx, num1, num2):
        num = random.randint(int(num1),int(num2))
        await ctx.send(f"{num} is your special number")

    @commands.command(aliases = ['8ball'])
    async def _8ball(self,ctx, *, question):
        responses = ["As I see it, yes",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",
                    "Don’t count on it",
                    "It is certain",
                    "It is decidedly so",
                    "Most likely",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Outlook good",
                    "Reply hazy, try again",
                    "Signs point to yes",
                    "Very doubtful",
                    "Without a doubt",
                    "Yes",
                    "Yes – definitely",
                    " You may rely on it"
                ]
        await ctx.send(f"{ctx.message.author.mention}'s Question: {question}\nOutlook: {random.choice(responses)}")

    @commands.command(aliases = ["flip", "cf", "coin_flip"])
    async def coinflip(self,ctx):
        coin = random.randint(0, 1)
        if(coin > 0):
            await ctx.send(f"Heads!")
        else:
            await ctx.send(f"Tails")

def setup(client):
    client.add_cog(Randomness(client))