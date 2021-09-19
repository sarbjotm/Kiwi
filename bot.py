import discord
import os
import mysql.connector
import datetime
from discord.ext import commands, tasks
# so we only have to load the word lists into memory one time -> ~0.22MB total
from myconstants import rolesList, activateRoles, load_data

load_data()

# --------------------------------------------------------------------------- #
# Test cases -- uncomment when testing

# from cogs.games import test
# test()

# --------------------------------------------------------------------------- #


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=',', intents=intents)
client.remove_command('help')


@client.command()
@commands.guild_only()
@commands.has_any_role("Dodo Op")
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.guild_only()
@commands.has_any_role("Dodo Op")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" to ,help"))
    print("Kiwi is Ready")
    wishbirthday.start()


@tasks.loop(minutes=1440)
async def wishbirthday():
    current_date = str(datetime.datetime.now())
    current_date = current_date[5:7] + current_date[8:10]
    guild = client.get_guild(744817281871249428)
    channel = guild.get_channel(755511228654420121)
    db = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    c = db.cursor()
    c.execute(f"""SELECT id
                FROM dodos
                WHERE birthday = {current_date}""")
    birthday_dodos = c.fetchall()
    for i in range(0, len(birthday_dodos)):
        username = int(birthday_dodos[i][0])
        await channel.send(f"Happy Birthday <@{username}>!!")
    c.close()
    db.close()


@client.event
async def on_member_join(member):
    guild = client.get_guild(int(os.environ['GUILD']))
    channel = guild.get_channel(int(os.environ['GUILD']))
    if 'h0nde' in member.name.lower() or 'honde' in member.name.lower():
        await member.ban(reason='h0nde')
        return

    db = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )

    c = db.cursor()
    c.execute(f"""INSERT INTO dodos 
                  VALUES ('{member.id}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'0000',0,0,0,0,0,0,0)
              """)
    db.commit()
    c.close()
    db.close()
    await channel.send(f"Added {member} to database")


@client.event
async def on_command_error(ctx, error):
    guild = client.get_guild(int(os.environ['GUILD']))
    channel = guild.get_channel(int(os.environ['CHANNEL']))
    if ctx.message == ",hit":
        return
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"That command does not exist. Use ,help for a list of commands")
        await channel.send(f"{ctx.message.author} tried to use a command that does not exist {error}")


@client.command()
@commands.guild_only()
async def ping(ctx):
    await ctx.send(f"Pong {str(round(client.latency, 2))}!")


@client.command()
@commands.guild_only()
async def testingtesting(ctx, msg):
    await msg.channel.send(
        "Testing Some Stuff",
        components=[
            Button(style=ButtonStyle.blue, label="Blue"),
            Button(style=ButtonStyle.red, label="Red"),
            Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
        ],
    )

    res = await client.wait_for("button_click")
    if res.channel == msg.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.component.label} clicked'
        )


@client.command(pass_context=True)
@commands.guild_only()
async def help(ctx, category=''):
    category = str(category).lower()
    if category == 'astrology':
        embed = discord.Embed(title="Astrology and Birthday", description="**,horoscope zodiac** - This will return your \
            Daily Horoscope based off of your zodiac sign \n\n \
            **,birthday mmdd** - This will set your birthday! Kiwi will wish you a happy birthday on your special day",
                              color=0x66abf9)

    elif category == 'decision':
        embed = discord.Embed(title="Decision Making",
                              description="**,8ball question** - ask Kiwi a question \n\n**,coinflip** - flip a coin "
                                          "\n\n**,poll \"Question\" option1 option2 ... option10** - Display a poll "
                                          "with n (2 <= n <= 10) options or a yes/no without any options shown",
                              color=0x66abf9)

    elif category == 'economy':
        embed = discord.Embed(title="Economy",
                              description="**,bal** - View your balance \n\n**,buy quantity role** Buy a role \n\n "
                                          "**,daily** - Recieve between 1-1000 discord dollars \n\n**,give @User x** "
                                          "- Give @User x dodo dollars \n\n**,leaderboard** - See top 5 Richest Dodos "
                                          "\n\n **,sell quantity role** - sell your roles for money \n\n**,"
                                          "shop** - see prices for roles",
                              color=0x66abf9)

    elif category == 'help':
        embed = discord.Embed(title="Help",
                              description="**,help** - To view all categories otherwise do **,help category** for "
                                          "info regarding the specified category \n\n **,ping** - See if bot is "
                                          "offline \n\n",
                              color=0x66abf9)

    elif category == 'mention':
        embed = discord.Embed(title="Mention",
                              description="**,hugs @user** - Gives the selected user a hug \n\n**,hugsRole @role** - "
                                          "group hug \n\n **,waves @user** - waves at a user \n\n**,wavesRole @role** "
                                          "- waves at a group \n\n",
                              color=0x66abf9)

    elif category == 'minigames':
        embed = discord.Embed(title="Minigames",
                              description="**,blackjack bet** - Play blackjack with Kiwi! Bet is your betting amount "
                                          "\n\n**,cup bet** - Play the classic 'guess where the gem' is game, "
                                          "pick the right cup and win!"
                                          "\n\n**,trivia bet <safe_filter_off=false>** - Kiwi finds a random image"
                                          "online and 4 similar captions; you have to figure out which one is real!"
                                          "The safe filter is initially on, however if you turn it off kiwi can be more"
                                          "risky with their search terms.",
                              color=0x66abf9)

    elif category == 'misc':
        embed = discord.Embed(title="Misc",
                              description="**,randomnumber a b ** - display rng [a,b] \n\n**,kittyclap** - send a "
                                          "kittyclap",
                              color=0x66abf9)

    elif category == 'role':
        embed = discord.Embed(title="Role Based",
                              description="**,collect** - obtain a role! 12 hour cooldown \n\n**,activate role** - "
                                          "activate a ,collect role\n\n**,trade your role @user their role** - trade "
                                          "roles \n\n**,myroles** - display a list of your roles \n\n**,"
                                          "roles** - display a list of collectable roles \n\n **,hide role** - hide a "
                                          "role from your profile \n\n**,show role** - make a role appear on profile "
                                          "\n\n **,hideall** - hide all roles \n\n**,showall** - show all roles",
                              color=0x66abf9)

    elif category == 'string':
        embed = discord.Embed(title="String",
                              description="**,fw message** - add sparkles between words \n**,spaced message** - "
                                          "space out your message \n\n**,spongebob message** - SpOnGeBoB MeMe",
                              color=0x66abf9)

    elif category == "weather":
        embed = discord.Embed(title="Misc",
                              description="**,weather city** - Find out the weather in your city! Sometimes you might "
                                          "have to add the country code, eg: London,CA",
                              color=0x66abf9)

    else:
        embed = discord.Embed(title="Kiwi Bot | Information", description="Hello there! My name is Kiwi thank you for joining the Dodo Server. To see what commands I have enter one of the following commands \n\n \
            **,help Astrology** - To view commands based on Astrology such as zodiac and birthday \n\n\
            **,help Decision** - To view commands to help your decision making such as coinflip and 8ball \n\n\
            **,help Economy** - To view commands based on Economy such as daily and selling/buying roles \n\n\
            **,help Help** - To view help based commands such as help and ping \n\n\
            **,help Mention** - To view commands that allow you to interact with other members such as hug and wave \n\n\
            **,help Minigames** - To view commands that allow you to play games such as blackjack and cup shuffle \n\n\
            **,help Misc** - To view random commands such as kittyclap and random number picking \n\n\
            **,help Role** - To view commands based on Roles such as collecting and trading \n\n\
            **,help String** - To view commands that alter your messages such as sparkles and spaced \n\n\
            **,help Weather** - To view commands based on the Weather such as weather \n\n \
            To learn more about me use the command **,about**", color=0x66abf9)

    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def about(ctx):
    embed = discord.Embed(title="About",
                          description="Kiwi is one of SFU Dodo Club's mascots, and is also our main Discord bot. Kiwi "
                                      "is constantly being updated and is maintend by myself. Kiwi is currently being "
                                      "hosted on Heroku under a Hobby Plan and has an MySQL Database connected to it.",
                          color=0x66abf9)
    embed.set_author(name="Amander",
                     icon_url="https://i.pinimg.com/originals/81/d7/d0/81d7d0dac44a4689449748532aac9f37.png")
    embed.add_field(name="Discord", value="<@264645255427522560>", inline=True)
    embed.add_field(name="Email", value=f"{os.environ['EMAIL']}", inline=True)
    embed.add_field(name="Github", value='[https://github.com/sarbjotm/Kiwi](https://github.com/sarbjotm/Kiwi)',
                    inline=False)
    embed.add_field(name="Donations",
                    value=f"I fianace this bot personally. Donations will help offset my costs of running and "
                          f"maintaining the bot. \n\n **E-Transfer**: Email above \nPaypal:["
                          f"https://www.paypal.com/paypalme/amandersm](https://www.paypal.com/paypalme/amandersm)",
                    inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
else:
    print("ran the file in lint mode, exiting gracefully.")
