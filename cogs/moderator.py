import discord
from discord.ext import commands
import random
import os
pollOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Moderator(client))
