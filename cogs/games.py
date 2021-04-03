import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path


numbers = ["1","2","3","4","5","6","7","8","9","10","11"]
suits = ["🔸","🔹"]

#Mentions
class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['21'])
    async def blackjack(self,ctx,bet):
        bet = int(bet)
        if(bet < 1):
            await ctx.send("You must bet at least 1 Dodo Dollar")
        else:
            db = mysql.connector.connect(
                host= os.environ['HOST'],
                user = os.environ['USER'],
                password = os.environ['PASSWORD'],
                database = os.environ['DATABASE']
            )
            c = db.cursor()
            c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

            """)
            balance = ''.join(map(str,c.fetchall()[0]))
            if(bet > int(balance)):
                await ctx.send("You do not have that much money!")
            else:
                embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                userBlackjack = False
                userCards = []
                userInt = 0
                userSuit = ''
                userCard = ''
                userDescription = ''

                dealerCards = []
                dealerInt = 0
                dealerSuit = ''
                dealerCard = ''
                dealerDescription = ''

                for i in range(0,2):
                    userCard = random.choice(numbers)
                    userSuit = random.choice(suits)
                    userCards.append(userCard+userSuit)
                    userInt = userInt + int(userCard)
                    
                #Check for Auto Bust
                while (userInt == 22):
                    userCard = random.choice(numbers)
                    userSuit = random.choice(suits)
                    userInt = userInt - 11
                    userCards[2] = userCard+userSuit
                    userInt = userInt + int(userCard)
                
                #Check for instant blackjack
                if(userInt == 21):
                    userBlackjack = True
                    
                dealerCard = random.choice(numbers)
                dealerSuit = random.choice(suits)
                dealerCards.append(dealerCard+dealerSuit)
                dealerInt = dealerInt + int(dealerCard)

                for cards in userCards:
                    userDescription = userDescription + cards + " "
                
                for cards in dealerCards:
                    dealerDescription = dealerDescription + cards + " "
                

                userDescription = f"{userDescription} \n \nScore: {userInt}"
                dealerDescription = f"{dealerDescription} \n \nScore: {dealerInt}"
                embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                await ctx.send(embed=embed)
                
                while(userInt < 22 and userBlackjack == False):
                    if(userInt == 21):
                        break
                        
                    embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                    await ctx.send(f'Do you want to hit or stand? You have 10 seconds to decide, if you do not reply i will assume you stand. If you enter anything else you will stand')
                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout = 10,
                            check=lambda message: message.author == ctx.message.author \
                                and message.channel == ctx.channel 
                        )
                        #Update user who intiated trade
                        msg = msg.content.strip().lower()
                        if(msg == "hit"):
                            userDescription = ''
                            userCard = random.choice(numbers)
                            userSuit = random.choice(suits)
                            userCards.append(userCard+userSuit)
                            userInt = userInt + int(userCard)
                            for cards in userCards:
                                userDescription = userDescription + cards + " "
                            userDescription = f"{userDescription} \n \n Score: {userInt}"
                            embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                            embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                            await ctx.send(embed=embed)
                        else:
                            break

                    except asyncio.TimeoutError:
                        break

                embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                if(userInt >= 22):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"Bust! You have lost {str(bet)}", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                else:
                    while((dealerInt < userInt) and userBlackjack == False):
                        dealerDescription = ''
                        dealerCard = random.choice(numbers)
                        dealerSuit = random.choice(suits)
                        dealerCards.append(dealerCard+dealerSuit)
                        dealerInt = dealerInt + int(dealerCard)
                        for cards in dealerCards:
                            dealerDescription = dealerDescription + cards + " "
                        dealerDescription = f"{dealerDescription} \n \n Score: {dealerInt}"
                    
                    if(userBlackjack == True):
                        bet = bet * 2
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**Blackjack! You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    
                    if(dealerInt > userInt and dealerInt < 22):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have lost {str(bet)}! Kiwi wins!**",inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif(dealerInt == userInt):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have tied {str(bet)}! No one wins**", inline=False)
                        await ctx.send(embed=embed)

                    else:
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    del(userCards)
                    del(dealerCards)
         
            c.close()
            db.close()

    @blackjack.error
    async def blackjack_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Syntax for this command is: **,blackjack bet**")
        await channel.send(f"{ctx.message.author} experienced a error using blackjack") 
    

    @commands.command(aliases = ['cup'])
    async def cupshuffle(self,ctx,bet):
        bet = int(bet)
        if(bet < 1):
            await ctx.send("You must bet at least 1 Dodo Dollar")
        else:
            db = mysql.connector.connect(
                host= os.environ['HOST'],
                user = os.environ['USER'],
                password = os.environ['PASSWORD'],
                database = os.environ['DATABASE']
            )
            c = db.cursor()
            c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

            """)
            balance = ''.join(map(str,c.fetchall()[0]))
            if(bet > int(balance)):
                await ctx.send("You do not have that much money!")
            else:
                pass
                
        c.close()
        db.close()
    



        
def setup(client):
    client.add_cog(Games(client))