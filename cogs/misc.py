import discord
from discord.ext import commands
import random
import os
pollOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


class MiscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Poll Command
    @commands.command()
    async def poll(self, ctx, question, *options):
        size = len(options)
        # Yes or No Question so add thumbs up/down
        if size == 0:
            embed = discord.Embed(title=question, color=0xe392fe)
            embed.set_thumbnail(url="https://i.imgur.com/Yx2cH7O.png")
            embed.add_field(name="Poll", value=question, inline=True)
            sent = await ctx.send(embed=embed)
            await sent.add_reaction("👍")
            await sent.add_reaction("👎")
            await ctx.message.delete(delay=0)
        # Poll with options
        elif (len(options) >= 2) and (len(options) <= 10):
            description_embed = " "
            for i in range(0, len(options)):
                description_embed = description_embed + pollOptions[i] + " " + options[i] + "\n"

            embed = discord.Embed(title=question, color=0xe392fe)
            embed.set_thumbnail(url="https://i.imgur.com/Yx2cH7O.png")
            embed.add_field(name="Options", value=description_embed, inline=True)
            await ctx.message.delete(delay=0)
            sent = await ctx.send(embed=embed)
            # Add 1 2 3 4 ... options as reacts
            for i in range(0, len(options)):
                await sent.add_reaction(pollOptions[i])

        elif len(options) > 10:
            await ctx.send("The maximum number of options is 10")
        else:
            await ctx.send("The minimum amount of options is 2, if you are not asking a Yes/No Question")

    @poll.error
    async def poll_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occured. Syntax for this command are as followed \n **,poll \"Question\" Option1 Option2 ... Option10** \n **,poll \"Question\"** \n **,poll \"Question\" \"Option1 Space\" Option2 ...**")
        await channel.send(f"{ctx.message.author} experienced a error using poll")

    @commands.command(aliases=['rand'])
    async def randomnumber(self, ctx, num1, num2):
        if (num1.isdigit()) and (num2.isdigit()):
            if num1 > num2:
                num = random.randint(int(num2), int(num1))
            elif num2 > num1:
                num = random.randint(int(num1), int(num2))
            else:
                num = num1
            await ctx.send(f"{num} is your special number")
        else:
            await ctx.send(f"Error. Use whole numbers only, e.g ,rand 1 10")

    @randomnumber.error
    async def randomnumber_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Error Occurred. Syntax for this command is: **,rand x y** where x and y are integer values")
        await channel.send(f"{ctx.message.author} experienced a error using rand. {error}")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
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

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send(
            "Error Occurred. Syntax for this command is: **,8ball question** make sure you have asked a question")
        await channel.send(f"{ctx.message.author} experienced a error using 8ball. {error}")

    @commands.command(aliases=["flip", "cf", "coin_flip"])
    async def coinflip(self, ctx):
        coin = random.randint(0, 1)
        if coin > 0:
            await ctx.send(f"Heads!")
        else:
            await ctx.send(f"Tails")

    @commands.command(aliases=["travisclap"])
    async def kittyclap(self, ctx):
        await ctx.message.delete(delay=0)
        await ctx.send("<a:travisclap:774127234184511498>")

    @commands.is_owner()
    @commands.command(aliases=["a", "anon", "announce"])
    async def announcement(self, ctx, *, statement):
        await ctx.message.delete(delay=0)
        embed = discord.Embed(title="Announcement", description=statement, color=0xe392fe)
        embed.set_author(name="Kiwi",
                         icon_url="https://github.com/SFU-Dodo-Club/Kiwi/blob/main/kiwi.png")
        await ctx.send(embed=embed)

    @announcement.error
    async def announcement_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send(f"Error Occurred. Syntax for this command is: **,anon message**. Your specific error is {error}")
        await channel.send(f"{ctx.message.author} experienced a error using anon. {error}")


def setup(client):
    client.add_cog(MiscCommands(client))
