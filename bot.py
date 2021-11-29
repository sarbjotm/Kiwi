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


intents = nextcord.Intents.default()
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
    channel = guild.get_channel(int(os.environ['GUILD']))
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
    halloween_roles = ["Dodo Goblin", "Dodo Ghost", "Dodo Witch", "Dodo Pumpkin", "Dodo Skeleton"]
    role_assign = random.choices(halloween_roles)[0]
    print(role_assign)
    role = discord.utils.get(guild.roles, name=role_assign)
    await member.add_roles(role)
    await channel.send(f"Added {member} to database")


@client.event
async def on_command_error(ctx, error):
    guild = client.get_guild(int(os.environ['GUILD']))
    channel = guild.get_channel(int(os.environ['CHANNEL']))
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"That command does not exist. Use ,help for a list of commands")
        await channel.send(f"{ctx.message.author} tried to use a command that does not exist {error}")


@client.command()
@commands.guild_only()
async def ping(ctx):
    await ctx.reply(f"Pong {str(round(client.latency, 2))}!")


@client.command()
@commands.guild_only()
async def hit(ctx):
    pass


@client.group(invoke_without_command = True)
@commands.guild_only()
@client.command(pass_context=True)
async def help(ctx):
    embed = nextcord.Embed(title = "Help", description = "Use ,help <command> for extended information. [] means required parameters and {} means option parameters")
    embed.add_field(name="Astrology/Birthday", value="``birthday``, ``horoscope``")
    embed.add_field(name = "Economy", value = "``bal``, ``buy``, ``daily``, ``give``, ``keep``, ``leaderboard``, ``sell``, ``shop``")

    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


#Astrology/Birthday
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




#Economy
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
    embed = nextcord.Embed(title = "daily", description = "Daily is used to get server currency. You will gain between 1 and 1000 Dodo Dollars, but there is a small (~5%) chance to lose money. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",daily")
    embed.add_field(name="Example", value=",daily")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def keep(ctx):
    embed = nextcord.Embed(title = "keep", description = "Keep is used to sell all your roles, until your roles are <= to the number you specified. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",keep [quantity]")
    embed.add_field(name="Example", value=",keep 3")
    embed.add_field(name="Explanation", value=",This will sell all of your roles individually until all of your roles are 3 or less. ")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@help.command()
async def give(ctx):
    embed = nextcord.Embed(title = "give", description = "Give another server member money. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",give [@User] [amount]")
    embed.add_field(name="Example", value=",give @Amander 1160")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


@help.command()
async def leaderboard(ctx):
    embed = nextcord.Embed(title = "leaderboard", description = "See the top 5 richest Dodos on the server. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",leaderboard")
    embed.add_field(name="Example", value=",leaderboard")


@help.command()
async def sell(ctx):
    embed = nextcord.Embed(title = "sell", description = "Sell roles individually. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",sell [amount] [role]")
    embed.add_field(name="Example", value=",sell 2 Dodo Green")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)

@help.command()
async def sell(ctx):
    embed = nextcord.Embed(title = "shop", description = "View prices of the shop. As a reminder: [] means required parameters and {} means option parameters")
    embed.add_field(name = "Syntax", value = ",shop")
    embed.add_field(name="Example", value=",shop")
    embed.set_author(name="Kiwi", icon_url="https://raw.githubusercontent.com/Sarbjotm/Kiwi/main/kiwi.png")
    await ctx.send(embed=embed)


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
    embed.add_field(name="Email", value=f"{os.environ['EMAIL']}", inline=True)
    embed.add_field(name="Github", value='[https://github.com/SFU-Dodo-Club/Kiwi/](https://github.com/SFU-Dodo-Club/Kiwi/)',
                    inline=False)
    embed.add_field(name="Donations",
                    value=f"I finance this bot personally. Donations will help offset my costs of running and "
                          f"maintaining the bot. \n\n **E-Transfer**: Email above \nPaypal:["
                          f"https://www.paypal.com/paypalme/amandersm](https://www.paypal.com/paypalme/amandersm)",
                    inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    client.run(os.environ['TOKEN'])
else:
    print("ran the file in lint mode, exiting gracefully.")
