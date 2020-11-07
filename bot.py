import discord
import asyncio
import random
import time
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = ',')

@client.event
async def on_ready():
    print("Bot is Ready")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

@client.command(aliases = ['wave'])
async def waves(ctx,member : discord.Member):
    await ctx.message.delete(delay = 0)
    await ctx.send(f"{ctx.message.author.mention} waves to {member.mention}")
    await ctx.send("https://media.tenor.com/images/ba69533b59d3ceaae8775a0550ff8037/tenor.gif")

@client.command(aliases = ['hug'])
async def hugs(ctx,member : discord.Member):
    await ctx.message.delete(delay = 0)
    await ctx.send(f"{ctx.message.author.mention} gibs beeeeg hug to {member.mention}")
    await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")

@client.command(aliases = ['hugRole'])
async def hugsRole(ctx,role : discord.Role):
    await ctx.message.delete(delay = 0)
    await ctx.send(f"{ctx.message.author.mention} gibs beeeeg group hug to {role.mention}")
    await ctx.send("https://media.tenor.com/images/0a1652de311806ce55820a7115993853/tenor.gif")


@client.command(aliases = ['waveRole'])
async def wavesRole(ctx,role : discord.Role):
    await ctx.message.delete(delay = 0)
    await ctx.send(f"{ctx.message.author.mention} waves to {role.mention}")
    await ctx.send("https://media4.giphy.com/media/3pZipqyo1sqHDfJGtz/200.gif")

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

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
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
    await ctx.send(f"Question: {question}\nOutlook: {random.choice(responses)}")


@client.command(aliases = ["bringpeace"])
async def banAlly(ctx):
    await ctx.send('Yes let us ban Ally!! Let us also ban Kyle!!')

@client.command()
async def spongebob(ctx, *, message):
    new = list(message)
    for i in range(0,len(new)):
        if( i % 2 == 0):
            new[i] = new[i].upper()
            "".join(new[i])
        else:
            new[i] = new[i].lower()
            "".join(new[i])
    str1 = ''
    for i in new:
        str1 += i 
    await ctx.send(f"{str1}")

@tasks.loop(hours = 24)
async def goodAfternoon():
    message_channel = client.get_channel(744817323973804093)
    await message_channel.send("Good Evening!")

@goodAfternoon.before_loop
async def before():
    await client.wait_until_ready()

@client.command(aliases = ["fw"])
async def fireworks(ctx, *, message):
    emoji = "✨"
    messageList = message.split()
    fireworkString = ""
    for i in range(0, len(messageList)):
        if(i == len(messageList) - 1):
            fireworkString += messageList[i]
        else:
            fireworkString += (messageList[i] + emoji)
    await ctx.send(f"{fireworkString}")

f = open("specialCode.txt", "r")
Token = str(f.readline()).strip('\n')

goodAfternoon.start()
client.run(Token)