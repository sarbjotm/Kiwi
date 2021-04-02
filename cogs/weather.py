import discord
import os
from discord.ext import commands
import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup



#Weather Alterations
class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    #Horoscope function - get daily horoscope from horoscope.com based from zodiac sign
    @commands.command()
    async def weather(self,ctx,city):
        city = str(city)
        baseURL = str(os.environ['BASE_URL'])
        apiKey = str(os.environ['API_KEY'])
        completeUrl = baseURL + city + apiKey
        await ctx.send("PLACEHOLDER")
        response = requests.get(completeUrl)
        x = response.json()
        if x["cod"] != "404":

            y = x["main"]

            temperature = y["temp"]
            temperatureC = temperature - 273.15
            temperatureF = temperatureC * 9/5 + 32

            # store the value corresponding
            # to the "humidity" key of y
            humidity = y["humidity"]
        
            # store the value of "weather"
            # key in variable z
            z = x["weather"]
        
            # store the value corresponding 
            # to the "description" key at 
            # the 0th index of z
            weatherDescription = z[0]["description"]
            if("clouds" in weatherDescription):
                logo = "http://getdrawings.com/free-icon/cloudy-icon-62.png"
            elif("sun" in weatherDescription or "sunny" in weatherDescription):
                logo = "https://cdn3.iconfinder.com/data/icons/summertime-1/44/summertime-03-512.png"
            elif("snow" in weatherDescription):
                logo="https://www.freeiconspng.com/thumbs/snow-icon/blue-snow-icon-8.png"
            elif("rain" in weatherDescription or "showers" in weatherDescription):
                logo = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather07-512.png"
            else:
                logo = "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/63069/weather-icon-clipart-md.png"
            
            embed=discord.Embed(title="Kiwi Shop", color=0xe392fe)
            embed.set_thumbnail(url= logo)
            embed.add_field(name="Temperature in C", value=temperatureC, inline=True)
            embed.add_field(name="Temperature in F", value=temperatureF, inline=True)
            embed.add_field(name="Humidity", value=humidity, inline=True)
            embed.add_field(name="Description", value=weatherDescription, inline=True)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Could not find that city")

def setup(client):
    client.add_cog(Weather(client))