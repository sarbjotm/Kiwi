import nextcord
import os
import mysql.connector
import datetime
from nextcord.ext import commands, tasks
import random
from nextcord.utils import get
# so we only have to load the word lists into memory one time -> ~0.22MB total
from myconstants import rolesList, activateRoles, load_data

load_data()

# --------------------------------------------------------------------------- #
# Test cases -- uncomment when testing

# from cogs.games import test
# test()

# --------------------------------------------------------------------------- #


intents = nextcord.Intents.all()
nextcord.members = True
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
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=" ,help"))
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
    channel = guild.get_channel(int(os.environ['CHANNEL']))
    db = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    c = db.cursor()


    c.execute(f"""SELECT id
            FROM dodos
            WHERE id = {member.id}
            ORDER BY id""")
    
    users = c.fetchall() 
                  
    if len(users) == 0:
        c.execute(f"""INSERT INTO dodos 
                           VALUES ('{member.id}',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'0000')
                      """)
        db.commit()
        await channel.send(f"Added {member} to database")
    
    c.close()
    db.close()


@client.event
async def on_command_error(ctx, error):
    guild = client.get_guild(int(os.environ['GUILD']))
    channel = guild.get_channel(int(os.environ['CHANNEL']))
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"That command does not exist. Use ,help for a list of commands")
        await channel.send(f"{ctx.message.author} tried to use a command that does not exist {error}")


@commands.command()
@commands.guild_only()
async def leaderboard(self, ctx):
    db = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    c = db.cursor()
    c.execute(f"""SELECT id, money
            FROM dodos
            ORDER BY money DESC LIMIT 5""")
    leaders = c.fetchall()
    description_embed = ""
    
    for i in range(0, 5):
        position = i + 1
        username = int(leaders[i][0])
        username = await client.fetch_user(username)
        money = str(leaders[i][1])
        description_embed = description_embed + str(position) + ". " + username.display_name + ": " + str(money) + "\n"
    embed = nextcord.Embed(title="Richest Dodos", color=0xe392fe)
    embed.set_thumbnail(url="https://i.imgur.com/5wjePlr.png")
    embed.add_field(name="Top 5", value=description_embed, inline=True)
    await ctx.send(embed=embed)

    c.close()
    db.close()

@client.command()
@commands.guild_only()
async def ping(ctx):
    await ctx.reply(f"Pong {str(round(client.latency, 2))}!")


@client.group(invoke_without_command = True)
@commands.guild_only()
async def help(ctx):
    embed = nextcord.Embed(title = "Help", description = "Use ``,help <command>`` for extended information. \n[] means required parameters and {} means option parameters")
    embed.add_field(name="Astrology/Birthday", value="``birthday``, ``horoscope``")
    embed.add_field(name="Decision Making", value="``_8ball``, ``coinflip``, ``poll``")
    embed.add_field(name = "Economy", value = "``bal``, ``buy``, ``daily``, ``give``, ``keep``, ``leaderboard``, ``sell``, ``shop``")
    embed.add_field(name = "Help", value = "``help``, ``ping``")
    embed.add_field(name="Interactions", value="``hugs``, ``hugsRoles``, ``info``, ``waves``, ``wavesRoles``")
    embed.add_field(name="Moderations", value="``To be checked then added``")
    embed.add_field(name="Minigames", value="``blackjack``, ``cupshuffle``, ``trivia``")
    embed.add_field(name="Other", value="``fw``, ``outline``, ``spaced``, ``spongebob``, ``travisclap``, ``weather``")
    embed.add_field(name="Role Based", value="``activate``, ``collect``, ``hide``, ``hideall``, ``myroles``, ``roles``,  ``show``, ``showall``, ``trade``")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)
#
#

#Astrology/Birthday -----------------------

@help.command()
async def birthday(ctx):
    embed = nextcord.Embed(title = "Birthday", description = "Set your birthday! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",birthday [mmdd] OR ,setbirthday [mmdd]")
    embed.add_field(name="Example", value=",setbirthday 0930 \n,setbirthday 0105")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def horoscope(ctx):
    embed = nextcord.Embed(title = "Horoscope", description = "View your horoscope! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",horoscope [zodiac_sign] OR ,zodiac [zodiac_sign]")
    embed.add_field(name="Example", value=",zodiac libra")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Economy  -----------------------

@help.command()
async def bal(ctx):
    embed = nextcord.Embed(title = "Bal", description = "View how much money you have. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",bal")
    embed.add_field(name="Example", value=",bal ")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@help.command()
async def buy(ctx):
    embed = nextcord.Embed(title = "Buy", description = "Use buy to buy roles with your server currency. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",buy [quantity] [role name]")
    embed.add_field(name="Example", value=",buy 1 Dodo Green")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def daily(ctx):
    embed = nextcord.Embed(title = "Daily", description = "Daily is used to get server currency. You will gain between 1 and 1000 Dodo Dollars, but there is a small (~5%) chance to lose money. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",daily")
    embed.add_field(name="Example", value=",daily")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def keep(ctx):
    embed = nextcord.Embed(title = "Keep", description = "Keep is used to sell all your roles, until your roles are <= to the number you specified. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",keep [quantity]")
    embed.add_field(name="Example", value=",keep 3")
    embed.add_field(name="Explanation", value=",This will sell all of your roles individually until all of your roles are 3 or less. ")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@help.command()
async def give(ctx):
    embed = nextcord.Embed(title = "Give", description = "Give another server member money. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",give [@User] [amount]")
    embed.add_field(name="Example", value=",give @Amander 1160")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@help.command()
async def leaderboard(ctx):
    embed = nextcord.Embed(title = "Leaderboard", description = "See the top 5 richest Dodos on the server. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",leaderboard")
    embed.add_field(name="Example", value=",leaderboard")


@help.command()
async def sell(ctx):
    embed = nextcord.Embed(title = "Sell", description = "Sell roles individually. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",sell [amount] [role]")
    embed.add_field(name="Example", value=",sell 2 Dodo Green")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def shop(ctx):
    embed = nextcord.Embed(title = "Shop", description = "View prices of the shop. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",shop")
    embed.add_field(name="Example", value=",shop")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Help  -----------------------
# @help.command()
# async def help(ctx):
#     embed = nextcord.Embed(title = "Help", description = "View the previous help message. As a reminder: [] means required parameters and {} means option parameters")
#     embed.add_field(name = "Syntax", value = ",help")
#     embed.add_field(name="Example", value=",help")
#     embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
#     await ctx.send(embed=embed)

@help.command()
async def ping(ctx):
    embed = nextcord.Embed(title = "Ping", description = "See the response time of Kiwi. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",ping")
    embed.add_field(name="Example", value=",ping")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Interactions  -----------------------
@help.command()
async def hugs(ctx):
    embed = nextcord.Embed(title = "Hugs", description = "Give another user a hug! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",hugs [@User]")
    embed.add_field(name="Example", value=",hugs @Kiwi")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def hugsRole(ctx):
    embed = nextcord.Embed(title = "Group Hug", description = "Give a group hug to a role! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",hugsRole [@rolename]")
    embed.add_field(name="Example", value=",hugsRole @Dodo Proper")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def info(ctx):
    embed = nextcord.Embed(title = "Info", description = "View another users information. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",info [@User]")
    embed.add_field(name="Example", value=",info @Amander")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def waves(ctx):
    embed = nextcord.Embed(title = "Waves", description = "Give another user a wave! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",wave [@User]")
    embed.add_field(name="Example", value=",wave @Kiwi")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def wavesRole(ctx):
    embed = nextcord.Embed(title = "Group Wave", description = "Give a group hug to a role! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",wavesRole [@rolename]")
    embed.add_field(name="Example", value=",wavesRole @Dodo Proper")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

#Minigames  -----------------------
@help.command()
async def blackjack(ctx):
    embed = nextcord.Embed(title = "Blackjack", description = "Blackjack! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",21 [bet amount] OR ,blackjack [bet amount]")
    embed.add_field(name="Example", value=",21 500")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def cupshuffle(ctx):
    embed = nextcord.Embed(title = "Shuffle Cup Game!", description = "Guess where the trophy is! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",cups [bet amount] OR ,cupshuffle [bet amount]")
    embed.add_field(name="Example", value=",21 500")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def trivia(ctx):
    embed = nextcord.Embed(title = "Trivia", description = "Guess which picture matches the description. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",trivia [bet amount]")
    embed.add_field(name="Example", value=",trivia 1250")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Role Based  -----------------------
@help.command()
async def activate(ctx):
    embed = nextcord.Embed(title = "Activate", description = "Activate a collectable role! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",activate [role]")
    embed.add_field(name="Example", value=",activate Dodo Red")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def collect(ctx):
    embed = nextcord.Embed(title = "Collect", description = "Collect a collectable role! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",collect")
    embed.add_field(name="Example", value=",collect")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def hide(ctx):
    embed = nextcord.Embed(title = "Hide", description = "Hide a collectable role from your profile! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",hide [role name]")
    embed.add_field(name="Example", value=",hide Dodo Red")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def hideall(ctx):
    embed = nextcord.Embed(title = "Hide All", description = "Hide all of your collectable role from your profile! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",hideall")
    embed.add_field(name="Example", value=",hideall")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def myroles(ctx):
    embed = nextcord.Embed(title = "My Roles", description = "View your collectable role information! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",myroles")
    embed.add_field(name="Example", value=",myroles")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def roles(ctx):
    embed = nextcord.Embed(title = "Roles", description = "View all collectable role information! As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",roles")
    embed.add_field(name="Example", value=",roles")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def show(ctx):
    embed = nextcord.Embed(title = "Show Roles", description = "Show a collectable roles full name on your profile. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",show [role name]")
    embed.add_field(name="Example", value=",show Dodo Red")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def showall(ctx):
    embed = nextcord.Embed(title = "Show All Roles", description = "Show all collectable roles full name on your profile. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",showall")
    embed.add_field(name="Example", value=",showall")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def trade(ctx):
    embed = nextcord.Embed(title = "Trade", description = "Trade roles with another user. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",trade [your role] @User [users role]")
    embed.add_field(name="Example", value=",trade Dodo Copyright @Myeuki Dodo Red")
    embed.add_field(name="Explanation", value=",If Myeuki accepts she will get Dodo Copyright and will give Dodo Red to the user who initated the trade")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

#Decision Making -----------------------

@help.command()
async def _8ball(ctx):
    embed = nextcord.Embed(title = "8ball", description = "Ask Kiwi a question. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",8ball [question]")
    embed.add_field(name="Example", value=",8ball Should I drink water")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def coinflip(ctx):
    embed = nextcord.Embed(title = "Coin Flip", description = "Flip a Coin. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",coinflip")
    embed.add_field(name="Example", value=",coinflip \n,cf")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def poll(ctx):
    embed = nextcord.Embed(title = "Poll", description = "Create A Poll. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",poll [question] {Option 1} {Option 2} ... {Option 10}")
    embed.add_field(name="Example", value=",poll \"Should we Dance \" \n,poll \"What Movie\" Movie1 \"Movie 2 With Spaces\" ")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Other -----------------------
@help.command()
async def fw(ctx):
    embed = nextcord.Embed(title = "Fireworks", description = "Space out your message with sparkles. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",fw [sentence] ")
    embed.add_field(name="Example", value=",fw Hello World")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def outline(ctx):
    embed = nextcord.Embed(title = "Outline", description = "View courses outlines at SFU. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",outline [Course Abbrievation and Name]{Section}{\"next\"}")
    embed.add_field(name="Example", value=",outline CMPT120 \n,sfu CMPT120 D200\n,sfu CMPT120 D100 next")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def spaced(ctx):
    embed = nextcord.Embed(title = "Spaced", description = "Space out your message. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",space [sentence] ")
    embed.add_field(name="Example", value=",sp Hello World \n,sp Hello \n,spaced Good Morning")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def spongebob(ctx):
    embed = nextcord.Embed(title = "Spongebob", description = "Alternate your sentence with uppercase and lowercase. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",spongebob [sentence] ")
    embed.add_field(name="Example", value=",spongebob Hello World")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def travisclap(ctx):
    embed = nextcord.Embed(title = "Travis Clap", description = "Send a Travis Clap emoji. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",travisclap")
    embed.add_field(name="Example", value=",travisclap \n,kittyclap")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def weather(ctx):
    embed = nextcord.Embed(title = "Weather", description = "Check The Weather. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",weather [CityName,Country]")
    embed.add_field(name="Example", value=",weather Vancouver \n,Surrey,CA")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


# @commands.guild_only()
# async def help(ctx, category=''):
#     category = str(category).lower()
#
#
#
#     elif category == 'misc':
#         embed = nextcord.Embed(title="Misc",
#                               description="**,randomnumber a b ** - display rng [a,b] \n\n**,kittyclap** - send a "
#                                           "kittyclap",
#                               color=0x66abf9)
#
#
#
#
#     else:
#         embed = nextcord.Embed(title="Kiwi Bot | Information", description="Hello there! My name is Kiwi thank you for joining the Dodo Server. To see what commands I have enter one of the following commands \n\n \
#             **,help Astrology** - To view commands based on Astrology such as zodiac and birthday \n\n\
#             **,help Decision** - To view commands to help your decision making such as coinflip and 8ball \n\n\
#             **,help Economy** - To view commands based on Economy such as daily and selling/buying roles \n\n\
#             **,help Help** - To view help based commands such as help and ping \n\n\
#             **,help Mention** - To view commands that allow you to interact with other members such as hug and wave \n\n\
#             **,help Minigames** - To view commands that allow you to play games such as blackjack and cup shuffle \n\n\
#             **,help Misc** - To view random commands such as kittyclap and random number picking \n\n\
#             **,help Role** - To view commands based on Roles such as collecting and trading \n\n\
#             **,help String** - To view commands that alter your messages such as sparkles and spaced \n\n\
#             **,help Weather** - To view commands based on the Weather such as weather \n\n \
#             To learn more about me use the command **,about**", color=0x66abf9)
#
#     embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
#     await ctx.send(embed=embed)


@client.command(pass_context=True)
@commands.guild_only()
async def about(ctx):
    embed = nextcord.Embed(title="About",
                          description="Kiwi is one of SFU Dodo Club's mascots, and is also our main Discord bot. Kiwi "
                                      "is constantly being updated and is maintend by myself. Kiwi is currently being "
                                      "hosted on Heroku under a Hobby Plan and has an MySQL Database connected to it.",
                          color=0x66abf9)
    embed.set_author(name="Amander",
                     icon_url="https://i.pinimg.com/originals/81/d7/d0/81d7d0dac44a4689449748532aac9f37.png")
    embed.add_field(name="Discord", value="<@264645255427522560>", inline=True)
    embed.add_field(name="Github", value='[Kiwi Github Link](https://github.com/SFU-Dodo-Club/Kiwi/)',
                    inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
else:
    print("ran the file in lint mode, exiting gracefully.")
