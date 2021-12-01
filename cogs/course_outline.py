import nextcord
import requests
import datetime

from nextcord.ext import commands
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
from myconstants import zodiacSigns, zodiacAvatars


class Outline(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sfu'])
    @commands.guild_only()
    async def outline(self, ctx, course, section="D100", next=""):
        course_name = course[0:len(course) - 3]
        course_number = course[len(course) - 3:]
        year = str(datetime.datetime.today().year)
        current_month = datetime.datetime.today().month
        semester = "fall" if current_month >= 9 else "spring" if current_month <= 4 else "summer"

        if str(next).lower() == "next":
            year = year if semester != "fall" else current_year + 1
            semester = "spring" if current_month >= 9 else "summer" if current_month <= 4 else "fall"

        try:
            source = requests.get(
                f'http://www.sfu.ca/students/calendar/{year}/{semester}/courses/{course_name.lower()}/{course_number}',
                timeout=5)

        except Timeout:
            await ctx.send("Error accessing server data, please try again later")

        else:
            if source.status_code == 404:
                embed = nextcord.Embed(title="Course Not Found", description="404 Error: This course does not exist",
                                      color=0xa6192e)
                await ctx.send(embed=embed)
                return

            elif source.status_code != 200:
                embed = nextcord.Embed(title="Error Accessing Webpage", description=f"{source} error. Try again later",
                                      color=0xa6192e)
                await ctx.send(embed=embed)
                return

            soup = BeautifulSoup(source.text, 'lxml')
            course_description = soup.find_all('p')

            embed_description = course_description[1].get_text() + "\n"
            course_title = soup.find_all('h1')
            course_title = str(course_title[1].get_text()).split()
            embed_title = course_name.upper() + str(course_number).upper() + " " + section + " - "
            for i in range(0, len(course_title) - 3):
                embed_title = embed_title + course_title[i] + " "

            try:
                source = requests.get(
                    f'http://www.sfu.ca/outlines.html?2021/fall/{course_name.lower()}/{course_number}/{section}',
                    timeout=5).text

            except Timeout:
                await ctx.send("Error accessing server data, please try again later")

            else:
                soup = BeautifulSoup(source, 'lxml')

                time = soup.find("li", {"class": "course-times"})
                if time is None:
                    time = ["Course Times + Location:", "N/A"]
                else:
                    time = time.text.split()

                prereq = soup.find("li", {"class": "prereq"})
                if prereq is None:
                    prereq = ["Prerequisites:", "N/A"]
                else:
                    prereq = prereq.text.split()
                instructor = soup.find("li", {"class": "instructor"})

                if instructor is None:
                    instructor = ["Instructor:", "N/A"]
                else:
                    instructor = instructor.text.split()

                for i in range(0, len(prereq)):
                    embed_description = embed_description + prereq[i] + " "

                embed_description = embed_description + "\n \n"

                for i in range(0, len(instructor)):
                    embed_description = embed_description + instructor[i] + " "

                embed_description = embed_description + "\n \n"
                for i in range(0, len(time)):
                    if len(time[i]) > 2 and (time[i][0] + time[i][1] == "PM" or time[i][0] + time[i][1] == "AM"):
                        embed_description = embed_description + time[i][0] + time[i][1] + " " + time[i][2:]
                    else:
                        embed_description = embed_description + time[i] + " "

                    if time[i] == "Location:" or time[i] == "Burnaby" or time[i] == "Surrey":
                        embed_description = embed_description + "\n"

                embed_description = embed_description.strip(" ")
                embed = nextcord.Embed(title=embed_title, description=embed_description, color=0xa6192e)
                await ctx.send(embed=embed)

    # If user doesn't provide zodiac sign, or enters to many parametres
    @outline.error
    async def outline_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send(f"Error Occured. Make sure the class exists and is offered during {semester} {year}. Alternatively check if SFU has released class schedules.")
        await channel.send(f"{ctx.message.author} experienced a error using outline/sfu. {error}")


def setup(client):
    client.add_cog(Outline(client))
