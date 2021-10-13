import nextcord
from nextcord.ext import commands
import random
import os
from nextcord.ext.commands import has_permissions, has_role
from nextcord.utils import get
import re

from myconstants import pollOptions


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @has_permissions(manage_roles=True)
    @commands.command(aliases=['newrole'])
    @commands.guild_only()
    async def createrole(self, ctx, colour, *role):
        if get(ctx.guild.roles, name=f"{role}"):
            await ctx.send("Role already exists")
            return
        regex = "^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        p = re.compile(regex)
        if re.search(p, str(colour)):
            guild = ctx.guild
            colour_of_role = '0x' + str(colour)
            print(colour_of_role)
            await guild.create_role(name=role, color=nextcord.Colour(int(f'{colour}', 16)))
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
    @commands.guild_only()
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
    @commands.guild_only()
    async def mute(self, ctx, member: nextcord.Member, reason = None):
        role = nextcord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        channel = ctx.guild.get_channel(int(853152816398729286))
        if reason is None:
            reason = "N/A"
        await channel.send(f"{ctx.message.author} muted {member} for {reason}")
        embed = nextcord.Embed(title="Muted",description=f"You have been muted.\nReason: {reason}", color=0xff0000)
        await member.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")
        

    @commands.command()
    @commands.has_role('Dodo Op')
    @commands.guild_only()
    async def unmute(self, ctx, member: nextcord.Member):
        role = nextcord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        channel = ctx.guild.get_channel(int(853152816398729286))
        await channel.send(f"{ctx.message.author} unmuted {member}")
        embed = nextcord.Embed(title="Unmuted",description=f"You have been unmuted", color=0xff0000)
        await member.send(embed=embed)
        
    @mute.error
    async def unmute_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    @commands.guild_only()
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @purge.error
    async def purge_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    @commands.guild_only()
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        channel = ctx.guild.get_channel(int(853152816398729286))
        if reason is None:
            reason = "N/A"
        await channel.send(f"{ctx.message.author} banned {member} for {reason}")
        embed = nextcord.Embed(title="Banned",description=f"You have been banned.\nReason: {reason}", color=0xff0000)
        await member.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.send(f"{ctx.message.author} experienced a error. {error}")

    @commands.command()
    @commands.has_role('Dodo Op')
    @commands.guild_only()
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        await member.kick(reason=reason)
        channel = ctx.guild.get_channel(int(853152816398729286))
        if reason is None:
            reason = "N/A"
        await channel.send(f"{ctx.message.author} muted {member} for {reason}")
        embed = nextcord.Embed(title="Kicked",description=f"You have been kicked.\nReason: {reason}", color=0xff0000)
        await member.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("No Permissions")
        await channel.kick(f"{ctx.message.author} experienced a error. {error}")


def setup(client):
    client.add_cog(Moderator(client))
