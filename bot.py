import discord
import asyncio
import os
import random
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = ',')

@client.command()
async def load(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Bot is Ready")

@commands.command()
@commands.cooldown(1,1440, commands.BucketType.user)
async def collect(self,ctx):
    roles = ['Santa Dodo', 'Elf Dodo', 'Frosty The Snow Dodo', 'Gift Dodo', 'Grinch Dodo']
    roleAssign = random.choices(roles, weights = [5,5,10,30,50])
    await ctx.send(f'You have drawn the {roleAssign[0]} role! Your next chance to role is in 24 hours')
    await client.add_roles(ctx.message.author, roleAssign[0])

# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(777046531214671902)    
#     await channel.send(f"Welcome {member.mention}!")

# @client.event
# async def on_member_remove(member):
#     channel = client.get_channel(777046531214671902)    
#     await channel.send(f"Goodbye {member.display_name}")


#Blackbox
f = open("specialCode.txt", "r")
Token = str(f.readline()).strip('\n')
client.run(Token)
