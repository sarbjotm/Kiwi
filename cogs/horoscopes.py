import discord
from discord.ext import commands
import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup

# Each sign is referenced to a number assigned by horoscope.com, this goes to the end of sign =
zodiacSigns = {
    "aries": "1",
    "taurus": "2",
    "gemini": "3",
    "cancer": "4",
    "leo": "5",
    "virgo": "6",
    "libra": "7",
    "scorpio": "8",
    "sagittarius": "9",
    "capricorn": "10",
    "aquarius": "11",
    "pisces": "12"
}

zodiacAvatars = ["", "https://www.horoscope.com/images-US/signs/profile-aries.png",
                 "https://www.horoscope.com/images-US/signs/profile-taurus.png",
                 "https://www.horoscope.com/images-US/signs/profile-gemini.png",
                 "https://www.horoscope.com/images-US/signs/profile-cancer.png",
                 "https://www.horoscope.com/images-US/signs/profile-leo.png",
                 "https://www.horoscope.com/images-US/signs/profile-virgo.png",
                 "https://www.horoscope.com/images-US/signs/profile-libra.png",
                 "https://www.horoscope.com/images-US/signs/profile-scorpio.png",
                 "https://www.horoscope.com/images-US/signs/profile-sagittarius.png",
                 "https://www.horoscope.com/images-US/signs/profile-capricorn.png",
                 "https://www.horoscope.com/images-US/signs/profile-aquarius.png",
                 "https://www.horoscope.com/images-US/signs/profile-pisces.png"]


# Horoscope Alterations
class Horoscope(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Horoscope function - get daily horoscope from horoscope.com based from zodiac sign
    @commands.command(aliases=['zodiac'])
    async def horoscope(self, ctx, zodiac):
        # Convert inputted zodiac sign to lower, to access dictionary value
        sign = str(zodiac).lower()
        if sign in zodiacSigns:
            number = zodiacSigns.get(sign)
            try:
                source = requests.get(
                    f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={number}',
                    timeout=5).text
            except Timeout:
                await ctx.send("Could not establish a connection to server. Try again later")

            else:
                soup = BeautifulSoup(source, 'lxml')
                today_horoscope = soup.p.text
                today_horoscope = str(today_horoscope)
                today_horoscope = today_horoscope.replace("people", "dodos")
                today_horoscope = today_horoscope.replace("somebody", "some dodo")
                today_horoscope = today_horoscope.replace("person", "dodo")
                today_horoscope = today_horoscope.replace("People", "dodos")
                today_horoscope = today_horoscope.replace("Somebody", "some dodo")
                today_horoscope = today_horoscope.replace("Person", "dodo")
                today_horoscope = today_horoscope.replace(sign[0].upper() + sign[1:].lower(),
                                                        str(ctx.message.author)[:-5])

                today_love = soup.find("a", {"id": "src-horo-matchlove"}).text
                today_love = today_love.replace("\n", " ")

                today_friend = soup.find("a", {"id": "src-horo-matchfriend"}).text
                today_friend = today_friend.replace("\n", " ")

                today_career = soup.find("a", {"id": "src-horo-matchcareer"}).text
                today_career = today_career.replace("\n", " ")

                embed = discord.Embed(title=f"{sign[0].upper() + sign[1:].lower()} Horoscope",
                                      description=f" **Daily Horoscope** \n \n {today_horoscope} \n \n **Today's Compatibility** \n \n",
                                      color=0x968cec)
                embed.set_thumbnail(url=zodiacAvatars[int(number)])
                embed.add_field(name=f"**{today_love[0:5].strip()}** ❤", value=f"{today_love[7:].strip()}", inline=True)
                embed.add_field(name=f"**{today_friend[0:11].strip()}** 🌻", value=f"{today_friend[13:].strip()}",
                                inline=True)
                embed.add_field(name=f"**{today_career[0:7].strip()}** 💰", value=f"{today_career[9:].strip()}",
                                inline=True)
                embed.set_footer(text="https://www.horoscope.com/us/index.aspx")
                await ctx.send(embed=embed)
        else:
            await ctx.send("Not a valid zodiac sign")

    # If user doesn't provide zodiac sign, or enters to many parametres
    @horoscope.error
    async def horoscope_error(self, ctx, error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,horoscope zodiac_sign**")
        await channel.send(f"{ctx.message.author} experienced a error using horoscope")


def setup(client):
    client.add_cog(Horoscope(client))
