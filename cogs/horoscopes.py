import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


zodiacSigns = {
    "aries":"1",
    "taurus":"2",
    "gemini":"3",
    "cancer":"4",
    "leo":"6",
    "libra":"7",
    "scorpio":"8",
    "sagittarius":"9",
    "capricorn":"10",
    "aquarius":"11",
    "pisces":"12"
}


#Text Alterations
class Horoscopes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def horoscope(self,ctx, zodiac):
        sign = str(zodiac).lower()
        if sign in zodiacSigns:
            number = zodiacSigns.get(sign)
            source = requests.get(f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={number}').text
            soup = BeautifulSoup(source,'lxml')
            todayHoroscope = soup.p.text
            embed=discord.Embed(title=f"{sign[0].upper() + sign[1:].lower()}'s Horoscope For Today" , color=0x66abf9)
            embed.add_field(name=f"{ctx.message.author}", value=f"{todayHoroscope}", inline=True)
        else:
            await ctx.send("Not a valid zodiac sign")
    
    @horoscope.error
    async def horoscope(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,hide zodiac_sign**")
        await channel.send(f"{ctx.message.author} experienced a error using horoscope")  
      

def setup(client):
    client.add_cog(Horoscopes(client))