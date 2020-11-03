import discord
import asyncio
import random
import time
from discord.ext import commands

client = commands.Bot(command_prefix = '^')

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

@client.command(aliases = ['wave'])
async def waves(ctx,member : discord.Member):
    await ctx.message.delete(delay = 0.5)
    await ctx.send(f"{ctx.message.author.mention} waves to {member.mention}")
    await ctx.send("https://media4.giphy.com/media/3pZipqyo1sqHDfJGtz/source.gif")

@client.command(aliases = ['rand'])
async def randomnumber(ctx, num1, num2):
       num = random.randint(int(num1),int(num2))
       await ctx.send(f"{num} is your special number")

@client.command(aliases = ['remindme'])
async def reminder(ctx, rtime, *, reminder):
    await ctx.message.delete(delay = 0)
    await ctx.send(f"{ctx.message.author.mention} reminder has been set")
    time.sleep(int(rtime))
    await ctx.send(f"{ctx.message.author.mention} here is your reminder to {reminder}")

@client.command(aliases = ["bringpeace"])
async def banAlly(ctx):
    await ctx.send('Yes let us ban Ally!! Let us also ban Kyle!!')

<<<<<<< HEAD
f = open("specialCode.txt", "r")
Token = str(f.readline()).strip('\n')

client.run(Token)
=======
client.run('')
>>>>>>> 932677981eadf1df11d77165fd4164f449a7d983
