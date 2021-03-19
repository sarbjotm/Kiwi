import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

#Each sign is referenced to a number assigned by horoscope.com, this goes to the end of sign = 
zodiacSigns = {
    "aries":"1",
    "taurus":"2",
    "gemini":"3",
    "cancer":"4",
    "leo":"5",
    "virgo":"6",
    "libra":"7",
    "scorpio":"8",
    "sagittarius":"9",
    "capricorn":"10",
    "aquarius":"11",
    "pisces":"12"
}


#Horoscope Alterations
class Horoscope(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    #Horoscope function - get daily horoscope from horoscope.com based from zodiac sign
    @commands.command()
    async def horoscope(self,ctx, zodiac):
        #Convert inputted zodiac sign to lower, to access dictionary value
        sign = str(zodiac).lower()
        if sign in zodiacSigns:
            number = zodiacSigns.get(sign)
            source = requests.get(f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={number}').text
            soup = BeautifulSoup(source,'lxml')
            todayHoroscope = soup.p.text
            await ctx.send(f"{todayHoroscope}")
        else:
            await ctx.send("Not a valid zodiac sign")
    
    #If user doesn't provide zodiac sign, or enters to many parametres
    @horoscope.error
    async def horoscope_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Error Occured. Syntax for this command is: **,hide zodiac_sign**")
        await channel.send(f"{ctx.message.author} experienced a error using horoscope")  
    
    @commands.command()
    async def amandertestingembeds(self,ctx):
        embed=discord.Embed(title="Daily Horoscope", color=0x968cec)
        embed.set_footer(text="Anticipation is often as good as, if not better than, the actual event, Virgo. This is what you experience today as you and your partner plan an exciting getaway. It's a busy day, booking hotels and airline tickets, but it's fun, too. You and your mate are giddy with the excitement of it all. This is just what your relationship needs.")
        await ctx.send(embed=embed)


      

def setup(client):
    client.add_cog(Horoscope(client))