import nextcord
import os
from nextcord.ext import commands
import requests

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Weather function - get weather information
    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, city):
        city = str(city)
        base_url = str(os.environ['BASE_URL'])
        api_key = str(os.environ['API_KEY'])
        complete_url = base_url + city + api_key
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":

            y = x["main"]
            temperature = y["temp"]
            temperature_c = int(temperature - 273.15)
            temperature_f = int(temperature_c * 9 / 5 + 32)
            city = city[0].upper() + city[1:].lower()
            # store the value corresponding
            # to the "humidity" key of y
            humidity = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding 
            # to the "description" key at 
            # the 0th index of z
            weather_description = z[0]["description"]
            if "clouds" in weather_description:
                logo = "http://getdrawings.com/free-icon/cloudy-icon-62.png"
            elif "clear" in weather_description or "sun" in weather_description or "sunny" in weather_description:
                logo = "https://cdn3.iconfinder.com/data/icons/summertime-1/44/summertime-03-512.png"
            elif "snow" in weather_description:
                logo = "https://www.freeiconspng.com/thumbs/snow-icon/blue-snow-icon-8.png"
            elif "rain" in weather_description or "showers" in weather_description:
                logo = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather07-512.png"
            else:
                logo = "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/63069/weather-icon-clipart-md.png"

            embed = nextcord.Embed(title=f"Weather in {city}", color=0x6cf178)
            embed.set_thumbnail(url=logo)
            embed.add_field(name="Temperature in C", value=temperature_c, inline=True)
            embed.add_field(name="Temperature in F", value=temperature_f, inline=True)
            embed.add_field(name="Humidity in %", value=humidity, inline=True)
            embed.add_field(name="Description", value=weather_description, inline=True)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Could not find that city")

    @weather.error
    async def weather_error(self, ctx, error):
        channel = ctx.guild.get_channel(int(os.environ['CHANNEL']))
        await ctx.send("Syntax for this command is: **,weather city**")
        await channel.send(f"{ctx.message.author} experienced a error using weather. {error}")


def setup(client):
    client.add_cog(Weather(client))
