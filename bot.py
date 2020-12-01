import discord
import asyncio
import os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = ',')

@client.event
async def on_ready():
    print("Bot is Ready")

@client.event
async def on_member_join(member):
    channel = client.get_channel(777046531214671902)    
    await channel.send(f"Welcome {member.mention}!")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(777046531214671902)    
    await channel.send(f"Goodbye {member.display_name}")


#Adding Cogs to Bot
for filename in os.listdir("./cogs"):
    client.load_extension(f"cogs.{filename[:-3]}")

#Blackbox
f = open("specialCode.txt", "r")
Token = str(f.readline()).strip('\n')
goodAfternoon.start()
client.run(Token)
