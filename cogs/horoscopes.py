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
        embed.set_footer(text="Unmarried people may run into differences with loved ones over future planning. They need to refrain from stretching things too far. Married couples may enjoy together. On the family front, things seem good. If you are in a meaningful relationship, you might have some disagreements. Do try asserting your view non-aggressively. Try to maintain peace and harmony in the relationship. On the financial front, things may be strong, and at the end of the week, you may have a chance to gain monetarily. Businessmen may strike a big-ticket deal while salaried individuals may get useful guidance from their superiors. Students pursuing graduation may be well-focused while studying. They may make good progress. Students pursuing post-graduation may get help from their professors. Their progress might be good too. On the health front, everything remains good. Beware of an upper-body injury. Perform some exercises in the morning to remain in good health.")
        await ctx.send(embed=embed)


      

def setup(client):
    client.add_cog(Horoscope(client))