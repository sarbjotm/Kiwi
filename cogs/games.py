import discord
from datetime import datetime, timedelta
from discord.ext import commands
import os
import random
import asyncio
import mysql
from pathlib import Path


numbers = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
suits = ["🍇","🍉","🍒","🍍"]

#Mentions
class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['21'])
    async def blackjack(self,ctx,bet):
        cardsDictionary = {
            "A": 4,
            2: 4,
            3: 4,
            4: 4,
            5: 4,
            6: 4,
            7: 4,
            8: 4,
            9: 4,
            10: 4,
            "J": 4,
            "Q": 4,
            "K": 4
            }
        

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
                userInt2 = 0
                userSuit = ''
                userCard = ''
                userDescription = ''

                dealerBlackjack = False
                mysteryScore = 0
                mysteryScore2 = 0
                dealerCards = []
                dealerInt = 0
                dealerInt2 = 0
                dealerSuit = ''
                dealerCard = ''
                dealerDescription = ''

                for i in range(0,2):
                    userCard = random.choice(numbers)
                    while(cardsDictionary[userCard] == 0):
                        userCard = random.choice(numbers)

                    cardsDictionary[userCard] = cardsDictionary[userCard] - 1
                    userSuit = random.choice(suits)
                    while(str(userCard)+userSuit in userCards or str(userCard)+userSuit in dealerCards):
                        userSuit = random.choice(suits)

                    userCards.append(str(userCard)+userSuit)
                    if(userCard == "J" or userCard == "K" or userCard == "Q"):
                        userCard = 10
                        userInt = userInt + 10
                        userInt2 = userInt2 + 10
                    elif(userCard == "A"):
                        userInt = userInt + 1
                        if(userInt2 + 11 <= 21):
                            userInt2 = userInt2 + 11
                        else:
                            userInt2 = userInt2 + 1
                    else:
                        userInt = userInt + userCard
                        userInt2 = userInt2 + userCard
                    

                    
                #Check for instant blackjack
                if(userInt == 21 or userInt2 == 21):
                    userBlackjack = True
                
                for i in range(0,2):
                    dealerCard = random.choice(numbers)
                    while(cardsDictionary[dealerCard] == 0):
                        dealerCard = random.choice(numbers)

                    cardsDictionary[dealerCard] = cardsDictionary[dealerCard] - 1
                    dealerSuit = random.choice(suits)
                    while(str(dealerCard)+dealerSuit in userCards or str(dealerCard)+dealerSuit in dealerCards):
                        dealerSuit = random.choice(suits)
                    dealerCards.append(str(dealerCard)+dealerSuit)
                    if(dealerCard == "J" or dealerCard == "K" or dealerCard == "Q"):
                        dealerCard = 10
                        dealerInt = dealerInt + 10
                        dealerInt2 = dealerInt2 + 10
                    elif(dealerCard == "A"):
                        dealerInt = dealerInt + 1
                        if(dealerInt2 + 11 <= 21):
                            dealerInt2 = dealerInt2 + 11
                        else:
                            dealerInt2 = dealerInt2 + 1
                    else:
                        dealerInt = dealerInt + dealerCard
                        dealerInt2 = dealerInt2 + dealerCard

                    if(i == 0):
                        mysteryScore = mysteryScore + dealerInt
                        if(mysteryScore == 1):
                            mysteryScore2 = mysteryScore2 + dealerInt2
                        else:
                            mysteryScore2 = mysteryScore2 + dealerInt
                
                #Check for instant blackjack
                if(dealerInt == 21 or dealerInt2 == 21):
                    dealerBlackjack = True
    

                for cards in userCards:
                    userDescription = userDescription + cards + " "
                
                dealerDescription = dealerDescription + dealerCards[0] + " [ ]"
                

                userDescription = f"{userDescription} \n \nScore: {userInt} \n \n Score 2: {userInt2}"
                dealerDescription = f"{dealerDescription} \n \nScore: {mysteryScore} \n \n Score 2: {mysteryScore2}"
                embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                await ctx.send(embed=embed)
                
                while(userInt < 22 and userInt2 < 22 and userBlackjack == False):
                    if(userInt == 21 or userInt2 == 21):
                        break
                    embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                    await ctx.send(f'Do you want to hit or stand? You have 20 seconds to decide, if you do not reply i will assume you stand. If you enter anything else you will stand')
                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout = 20,
                            check=lambda message: message.author == ctx.message.author \
                                and message.channel == ctx.channel 
                        )
                        
                        msg = msg.content.strip().lower()
                        if(msg == "hit"):
                            userDescription = ''
                            userCard = random.choice(numbers)
                            while(cardsDictionary[userCard] == 0):
                                userCard = random.choice(numbers)
                            
                            cardsDictionary[userCard] = cardsDictionary[userCard] - 1
                            userSuit = random.choice(suits)
                            while(str(userCard)+userSuit in userCards or str(userCard)+userSuit in dealerCards):
                                userSuit = random.choice(suits)
                            userCards.append(str(userCard)+userSuit)
                            if(userCard == "J" or userCard == "K" or userCard == "Q"):
                                userCard = 10
                                userInt = userInt + 10
                                userInt2 = userInt2 + 10
                            elif(userCard == "A"):
                                userInt = userInt + 1
                                if(userInt2 + 11 <= 21):
                                    userInt2 = userInt2 + 11
                                else:
                                    userInt2 = userInt2 + 1
                            else:
                                userInt = userInt + userCard
                                userInt2 = userInt2 + userCard

                            for cards in userCards:
                                userDescription = userDescription + cards + " "
                            userDescription = f"{userDescription} \n \n Score: {userInt} \n \n Score2: {userInt2}"
                            embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                            embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                            await ctx.send(embed=embed)
                        else:
                            break

                    except asyncio.TimeoutError:
                        break

                embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                if(userInt >= 22 and userInt2 >= 22):
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
                    if (userInt >= 22 and userInt2 <= 21):
                        temp = userInt
                        userInt = userInt2
                        userInt2 = temp
                
                    elif(userInt2 >= 22 and userInt <= 21):
                        userInt = userInt
                    
                    elif(userInt2 > userInt):
                        temp = userInt
                        userInt = userInt2
                        userInt2 = temp
                    else:
                        userInt = userInt

                    if(userBlackjack == False and dealerBlackjack == False):
                        while(1):
                            if( (dealerInt >= 22) and (dealerInt2 >= 22) ):
                                break
                            elif(dealerInt >= 17 or dealerInt2 >= 17):
                                break
                            else:
                                dealerDescription = ''
                                dealerCard = random.choice(numbers)
                                while(cardsDictionary[dealerCard] == 0):
                                    dealerCard = random.choice(numbers)
                                cardsDictionary[dealerCard] = cardsDictionary[dealerCard] - 1
                                dealerSuit = random.choice(suits)
                                while(str(dealerCard)+dealerSuit in userCards or str(dealerCard)+dealerSuit in dealerCards):
                                    dealerSuit = random.choice(suits)
                                dealerCards.append(str(dealerCard)+dealerSuit)
                                if(dealerCard == "J" or dealerCard == "K" or dealerCard == "Q"):
                                    dealerCard = 10
                                    dealerInt = dealerInt + 10
                                    dealerInt2 = dealerInt2 + 10
                                elif(dealerCard == "A"):
                                    dealerInt = dealerInt + 1
                                    if(dealerInt2 + 11 <= 21):
                                        dealerInt2 = dealerInt2 + 11
                                    else:
                                        dealerInt2 = dealerInt2 + 1  
                                else:
                                    dealerInt = dealerInt + dealerCard
                                    dealerInt2 = dealerInt2 + dealerCard
                                
                                for cards in dealerCards:
                                    dealerDescription = dealerDescription + cards + " "
                                dealerDescription = f"{dealerDescription} \n \n Score: {dealerInt} \n \n Score2: {dealerInt2}"
                        
                    if (dealerInt >= 22 and dealerInt2 <= 21):
                        temp = dealerInt
                        dealerInt = dealerInt2
                        dealerInt2 = temp
                
                    elif(dealerInt2 >= 22 and dealerInt <= 21):
                        userInt = userInt
                    
                    elif(dealerInt2 > dealerInt):
                        temp = dealerInt
                        dealerInt = dealerInt2
                        dealerInt2 = temp
                    else:
                        dealerInt = dealerInt

                    embed=discord.Embed(title= "Dodo Club Casino | Blackjack", color=0x99c0dd)
                    dealerDescription = ' '
                    for cards in dealerCards:
                        dealerDescription = dealerDescription + cards + " "
                    dealerDescription = f"{dealerDescription} \n \n Score: {dealerInt} \n \n Score2: {dealerInt2}"
                    if(dealerBlackjack == True and userBlackjack == True):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**Well this is awkward... both of us got blackjack. No one wins**", inline=False)
                        await ctx.send(embed=embed)

                    elif(userBlackjack == True):
                        bet = bet * 2
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**Blackjack! You have won {str(bet)} Dodo Dollars!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    
                    elif(dealerBlackjack == True):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    
                    elif(dealerInt > userInt and dealerInt < 22):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif(dealerInt == userInt):
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{userDescription}" , inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealerDescription}" , inline=True)
                        embed.add_field(name = f"Outcome", value=f"**You have tied! No one wins**", inline=False)
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

                    print(cardsDictionary)
                    del(userCards)
                    del(dealerCards)
         
            c.close()
            db.close()

    @blackjack.error
    async def blackjack_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Syntax for this command is: **,blackjack bet**. Currently command is mod only while adding card count")
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
                gem = random.randint(1,3)
                embedDescription = "Which Kiwi has the hidden gem \n 🥝 🥝 🥝"
                endingDescription = ""
                embed=discord.Embed(title= "Dodo Club Casino | Cup Shuffle", description = embedDescription, color=0x99c0dd)
                await ctx.send(embed=embed)
                await ctx.send(f'Which Kiwi would you like to pick 1, 2, 3? If you do not answer in 20 seconds I will randomly pick for you')

                try:
                    msg = await self.client.wait_for(
                        "message",
                        timeout = 20,
                        check=lambda message: message.author == ctx.message.author \
                            and message.channel == ctx.channel 
                    )
                    msg = msg.content.strip().lower()
                    try:
                        msg = int(msg)
                    except:
                        await ctx.send("Gonna give you a random variable for not following rules.")
                        msg = random.randint(1,4)
                    if(msg == gem):
                        for i in range(1,4):
                            if(i == gem):
                                endingDescription = endingDescription + "🏆 "
                            else:
                                endingDescription = endingDescription + "🥝 " 
                        embed=discord.Embed(title= "Dodo Club Casino | Cup Shuffle",description = endingDescription, color=0x99c0dd)
                        embed.add_field(name = f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    else:
                        for i in range(1,4):
                            if(i == gem):
                                endingDescription = endingDescription + "🏆 "
                            elif(i == msg):
                                endingDescription = endingDescription + "❌ "
                            else:
                                endingDescription = endingDescription + "🥝 " 
                        embed=discord.Embed(title= "Dodo Club Casino | Cup Shuffle",description = endingDescription, color=0x99c0dd)
                        embed.add_field(name = f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                            

                except asyncio.TimeoutError:
                    userGuess = random.randint(1,3)
                    await ctx.send(f"Assuming you meant to guess kiwi number: {userGuess}")
                    if(userGuess == gem):
                        for i in range(1,4):
                            if(i == gem):
                                endingDescription = endingDescription + "🏆 "
                            else:
                                endingDescription = endingDescription + "🥝 "
                        embed=discord.Embed(title= "Dodo Club Casino | Cup Shuffle",description = endingDescription, color=0x99c0dd)
                        embed.add_field(name = f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                    else:
                        for i in range(1,4):
                            if(i == gem):
                                endingDescription = endingDescription + "🏆 "
                            elif(i == userGuess):
                                endingDescription = endingDescription + "❌ "
                            else:
                                endingDescription = endingDescription + "🥝 "
                        embed=discord.Embed(title= "Dodo Club Casino | Cup Shuffle",description = endingDescription, color=0x99c0dd)
                        embed.add_field(name = f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()
                
            c.close()
            db.close()
    

    @cupshuffle.error
    async def cupshuffle_error(self,ctx,error):
        channel = ctx.guild.get_channel(800965152132431892)
        await ctx.send("Syntax for this command is: **,cupshuffle bet**")
        await channel.send(f"{ctx.message.author} experienced a error using cupshuffle") 

        
def setup(client):
    client.add_cog(Games(client))