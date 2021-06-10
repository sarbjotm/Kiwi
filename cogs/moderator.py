import discord
from discord.ext import commands
import random
import os
from discord.ext.commands import has_permissions, has_role
from discord.utils import get
import re

from myconstants import pollOptions


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @has_permissions(manage_roles=True)
    @commands.command()
    async def createrole(self, ctx, colour, *, role):
        if get(ctx.guild.roles, name=f"{role}"):
            await ctx.send("Role already exists")
            return
        regex = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        p = re.compile(regex)
        if re.search(p, str(colour)):
            guild = ctx.guild
            colour_of_role = '0x' + str(colour)
            print(colour_of_role)
            await guild.create_role(name=role, color=discord.Colour(int(f'{colour}', 16)))
            print("role Created")
            await ctx.send(f"{role} created with colour code {colour_of_role}")
        else:
            await ctx.send("Enter a valid hex colour code")

    @createrole.error
    async def createrole_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def echo(self, ctx, *, statement):
        await ctx.message.delete(delay=0)
        await ctx.send(f"{statement}")

    @echo.error
    async def echo_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)

    @mute.error
    async def mute_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)

    @mute.error
    async def unmute_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @purge.error
    async def purge_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.kick(f"{ctx.message.author} experienced a error. {error}")


def setup(client):
    client.add_cog(Moderator(client))
