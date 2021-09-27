import os, random, asyncio, requests
import mysql

from discord.ext import commands
import discord

from bs4 import BeautifulSoup

from myconstants import numbers, suits, words_10k, words_20k_includes_swears
from dbcontroller import connect_to_db, close_db, get_balance, update_money
from async_util import wait_for_response

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['21'])
    @commands.guild_only()
    async def blackjack(self, ctx, bet):
        cards_dictionary = {
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
        if bet <= 0:
            await ctx.send("You must bet at least 1 Dodo Dollar")
            return
        else:
            db = mysql.connector.connect(
                host=os.environ['HOST'],
                user=os.environ['USER'],
                password=os.environ['PASSWORD'],
                database=os.environ['DATABASE']
            )
            c = db.cursor()
            c.execute(f"""SELECT money
                        FROM dodos
                        WHERE id = {ctx.message.author.id}

            """)
            balance = ''.join(map(str, c.fetchall()[0]))
            if bet > int(balance):
                await ctx.send("You do not have that much money!")
            else:
                embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                user_blackjack = False
                user_cards = []
                user_int = 0
                user_int2 = 0
                user_description = ''

                dealer_blackjack = False
                mystery_score = 0
                mystery_score2 = 0
                dealer_cards = []
                dealer_int = 0
                dealer_int2 = 0
                dealer_description = ''

                for i in range(0, 2):
                    user_card = random.choice(numbers)
                    while cards_dictionary[user_card] == 0:
                        user_card = random.choice(numbers)

                    cards_dictionary[user_card] = cards_dictionary[user_card] - 1
                    user_suit = random.choice(suits)
                    while str(user_card) + user_suit in user_cards or str(user_card) + user_suit in dealer_cards:
                        user_suit = random.choice(suits)

                    user_cards.append(str(user_card) + user_suit)
                    if user_card == "J" or user_card == "K" or user_card == "Q":
                        user_int = user_int + 10
                        user_int2 = user_int2 + 10
                    elif user_card == "A":
                        user_int = user_int + 1
                        if user_int2 + 11 <= 21:
                            user_int2 = user_int2 + 11
                        else:
                            user_int2 = user_int2 + 1
                    else:
                        user_int = user_int + user_card
                        user_int2 = user_int2 + user_card

                    dealer_card = random.choice(numbers)
                    while cards_dictionary[dealer_card] == 0:
                        dealer_card = random.choice(numbers)

                    cards_dictionary[dealer_card] = cards_dictionary[dealer_card] - 1
                    dealer_suit = random.choice(suits)
                    while str(dealer_card) + dealer_suit in user_cards or str(dealer_card) + dealer_suit in dealer_cards:
                        dealer_suit = random.choice(suits)
                    dealer_cards.append(str(dealer_card) + dealer_suit)
                    if dealer_card == "J" or dealer_card == "K" or dealer_card == "Q":
                        dealer_int = dealer_int + 10
                        dealer_int2 = dealer_int2 + 10
                    elif dealer_card == "A":
                        dealer_int = dealer_int + 1
                        if dealer_int2 + 11 <= 21:
                            dealer_int2 = dealer_int2 + 11
                        else:
                            dealer_int2 = dealer_int2 + 1
                    else:
                        dealer_int = dealer_int + dealer_card
                        dealer_int2 = dealer_int2 + dealer_card

                    if i == 0:
                        mystery_score = mystery_score + dealer_int
                        if mystery_score == 1:
                            mystery_score2 = mystery_score2 + dealer_int2
                        else:
                            mystery_score2 = mystery_score2 + dealer_int

                # Check for instant blackjack
                if user_int == 21 or user_int2 == 21:
                    user_blackjack = True

                    # Check for instant blackjack
                if dealer_int == 21 or dealer_int2 == 21:
                    dealer_blackjack = True

                for cards in user_cards:
                    user_description = user_description + cards + " "

                # initial setup to show face down card
                dealer_description = dealer_description + dealer_cards[0] + " [ ]"

                user_description = f"{user_description} \n \nScore: {user_int} or {user_int2}"
                dealer_description = f"{dealer_description} \n \nScore: {mystery_score} or {mystery_score2}"
                embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}", inline=True)
                embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                embed.add_field(name=f"What would you like to do? You have 20 seconds to decide", value="Enter Hit or Stand",
                                inline=False)
                game_message = await ctx.send(embed=embed)

                while 1:
                    if user_int >= 22 and user_int2 >= 22:
                        break

                    elif user_int == 21 or user_int2 == 21:
                        break

                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout=20,
                            check=lambda message: message.author == ctx.message.author and message.channel == ctx.channel
                        )

                        msg_str = msg.content.strip().lower()
                        if msg_str == "hit" or msg_str == ",hit":
                            embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x99c0dd)
                            user_description = ''
                            user_card = random.choice(numbers)
                            while cards_dictionary[user_card] == 0:
                                user_card = random.choice(numbers)

                            cards_dictionary[user_card] = cards_dictionary[user_card] - 1
                            user_suit = random.choice(suits)
                            while str(user_card) + user_suit in user_cards or str(user_card) + user_suit in dealer_cards:
                                user_suit = random.choice(suits)
                            user_cards.append(str(user_card) + user_suit)
                            if user_card == "J" or user_card == "K" or user_card == "Q":
                                user_int = user_int + 10
                                user_int2 = user_int2 + 10
                            elif user_card == "A":
                                user_int = user_int + 1
                                if user_int2 + 11 <= 21:
                                    user_int2 = user_int2 + 11
                                else:
                                    user_int2 = user_int2 + 1
                            else:
                                user_int = user_int + user_card
                                user_int2 = user_int2 + user_card

                            for cards in user_cards:
                                user_description = user_description + cards + " "
                            user_description = f"{user_description} \n \n Score: {user_int} or {user_int2}"
                            embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                            inline=True)
                            embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                            embed.add_field(name=f"What would you like to do? You have 20 seconds to decide",
                                            value="Enter Hit or Stand", inline=False)
                            await msg.delete(delay=0)
                            await game_message.edit(embed=embed)
                        else:
                            await msg.delete(delay=0)
                            break

                    except asyncio.TimeoutError:
                        break

                if user_int >= 22 and user_int2 >= 22:
                    embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0xfd4f58)
                    embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                    inline=True)
                    embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                    embed.add_field(name=f"Outcome", value=f"**Bust! You have lost {str(bet)}**", inline=False)
                    await game_message.edit(embed=embed)
                    c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                    db.commit()

                else:
                    if user_int <= user_int2 <= 21 or user_int2 <= 21 < user_int:
                        user_int = user_int2

                    if user_blackjack is False and dealer_blackjack is False:
                        while 1:
                            if (dealer_int >= 22) and (dealer_int2 >= 22):
                                break
                            elif dealer_int >= 17 and dealer_int2 >= 17:
                                break
                            elif dealer_int >= user_int:
                                break
                            else:
                                dealer_card = random.choice(numbers)
                                while cards_dictionary[dealer_card] == 0:
                                    dealer_card = random.choice(numbers)
                                cards_dictionary[dealer_card] = cards_dictionary[dealer_card] - 1
                                dealer_suit = random.choice(suits)
                                while str(dealer_card) + dealer_suit in user_cards or str(dealer_card) + dealer_suit in dealer_cards:
                                    dealer_suit = random.choice(suits)
                                dealer_cards.append(str(dealer_card) + dealer_suit)
                                if dealer_card == "J" or dealer_card == "K" or dealer_card == "Q":
                                    dealer_int = dealer_int + 10
                                    dealer_int2 = dealer_int2 + 10
                                elif dealer_card == "A":
                                    dealer_int = dealer_int + 1
                                    if dealer_int2 + 11 <= 21:
                                        dealer_int2 = dealer_int2 + 11
                                    else:
                                        dealer_int2 = dealer_int2 + 1
                                else:
                                    dealer_int = dealer_int + dealer_card
                                    dealer_int2 = dealer_int2 + dealer_card

                    if dealer_int <= dealer_int2 <= 21 or dealer_int2 <= 21 < dealer_int:
                        temp = dealer_int
                        dealer_int = dealer_int2
                        dealer_int2 = temp

                    dealer_description = ' '
                    for cards in dealer_cards:
                        dealer_description = dealer_description + cards + " "
                    dealer_description = f"{dealer_description} \n \n Score: {dealer_int} or {dealer_int2}"

                    if user_blackjack is True:
                        embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x8ebd9d)
                        bet = bet * 2
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**Blackjack! You have won {str(bet)} Dodo Dollars!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif dealer_blackjack is True:
                        embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0xfd4f58)
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif user_int < dealer_int < 22:
                        embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0xfd4f58)
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)} Dodo Dollars! Kiwi wins!**",
                                        inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money - {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    elif dealer_int == user_int:
                        embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0xeecb76)
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have tied! No one wins**", inline=False)
                        await game_message.edit(embed=embed)

                    else:
                        embed = discord.Embed(title="Dodo Club Casino | Blackjack", color=0x8ebd9d)
                        embed.add_field(name=f"{str(ctx.message.author)[:-5]}'s Hand", value=f"{user_description}",
                                        inline=True)
                        embed.add_field(name=f"Kiwi's Hand", value=f"{dealer_description}", inline=True)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await game_message.edit(embed=embed)
                        c.execute(f"""UPDATE dodos
                        SET money = money + {bet}
                        WHERE id = {ctx.message.author.id}
                        """)
                        db.commit()

                    del user_cards
                    del dealer_cards

            c.close()
            db.close()

    @blackjack.error
    async def blackjack_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await channel.send(f"{ctx.message.author} experienced a error using blackjack. {error}")

    @commands.command(aliases=['cup', 'cups'])
    @commands.guild_only()
    async def cupshuffle(self, ctx, bet):
        bet = int(bet)
        if bet < 1:
            await ctx.send("You must bet at least 1 Dodo Dollar")
        else:
            user_id = ctx.message.author.id
            db, cur = connect_to_db()
            balance = get_balance(cur, user_id) 
            if bet > int(balance):
                await ctx.send("You do not have that much money!")
            else:
                gem = random.randint(1, 3)
                embed_description = "Which Kiwi has the hidden gem \n 🥝 🥝 🥝"
                ending_description = ""
                embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=embed_description,
                                      color=0x99c0dd)
                await ctx.send(embed=embed)
                await ctx.send(f'Which Kiwi would you like to pick 1, 2, 3? If you do not answer in 20 seconds '
                    'I will randomly pick for you.')

                try:
                    msg = await self.client.wait_for(
                        "message",
                        timeout=20,
                        check=lambda message: message.author == ctx.message.author and message.channel == ctx.channel
                    )
                    msg = msg.content.strip().lower()
                    try:
                        msg = int(msg)
                    except:
                        await ctx.send("Gonna give you a random variable for not following rules.")
                        msg = random.randint(1, 4)
                    if msg == gem:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)

                        update_money(db, cur, user_id, bet)
                    else:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            elif i == msg:
                                ending_description = ending_description + "❌ "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)

                        update_money(db, cur, user_id, -bet)

                except asyncio.TimeoutError:
                    user_guess = random.randint(1, 3)
                    await ctx.send(f"Assuming you meant to guess kiwi number: {user_guess}")
                    if user_guess == gem:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have won {str(bet)}!**", inline=False)
                        await ctx.send(embed=embed)

                        update_money(db, cur, user_id, bet)
                    else:
                        for i in range(1, 4):
                            if i == gem:
                                ending_description = ending_description + "🏆 "
                            elif i == user_guess:
                                ending_description = ending_description + "❌ "
                            else:
                                ending_description = ending_description + "🥝 "
                        embed = discord.Embed(title="Dodo Club Casino | Cup Shuffle", description=ending_description,
                                              color=0x99c0dd)
                        embed.add_field(name=f"Outcome", value=f"**You have lost {str(bet)}!**", inline=False)
                        embed.set_footer(text=f"Winning Kiwi was number {gem}")
                        await ctx.send(embed=embed)

                        update_money(db, cur, user_id, -bet)
                        
            close_db(cur, db)

    @cupshuffle.error
    async def cupshuffle_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Syntax for this command is: **,cupshuffle bet**")
        await channel.send(f"{ctx.message.author} experienced a error using cupshuffle. {error}")

    @commands.command(aliases=['match_image', 'img_match', 'match_img', 'trivia'])
    @commands.guild_only()
    async def image_match(self, ctx, bet, no_pain_no_gain=False):
        bet = int(bet)
        if bet < 1:
            await ctx.send("You must bet at least 1 Dodo Dollar")
        else:
            user_id = ctx.message.author.id
            db, cur = connect_to_db()
            balance = get_balance(cur, user_id) 
            if bet > int(balance):
                await ctx.send("You do not have that much money!")
                close_db(cur, db)
                return

            # collect 5 random title & img-src pairs. Choose 1 to be the main image.
            pairs = generate_random_images(5, False)
            target_i = random.randint(0, len(pairs)-1)
            target_pair = pairs[target_i]

            # TODO: utilize https://github.com/RobertJGabriel/Google-profanity-words and parse all the user facing 
            # content, then reject bad words. Repeat if neccesary. 

            # send an embed and wait 30s for answer -> send a followup message when there is only 10s left.
            line1 = "Which caption do you think corresponds to the following image?\n\n".format(bet)
            desc = "**Choice 1:** \t`{}` \n**Choice 2:** \t`{}` \n**Choice 3:** \t`{}` \n**Choice 4:** \t`{}` \n**Choice 5:** \t`{}`\n\n".format(
                pairs[0]["title"], pairs[1]["title"], pairs[2]["title"], pairs[3]["title"], pairs[4]["title"])
            end_line =  "You have 30s to respond with your choice of 1, 2, 3, 4, or 5."
            embed_msg = discord.Embed(
                title="Dodo Club Casino | Image Match Game", 
                description=line1+desc+end_line, 
                color=0x5ce6cc)

            # TODO: make it so that this image is downloaded then served, so that the website can't be easily traced.
            # Or just add a time-limit, but only when I finally decide to improve 
            embed_msg.set_image(url=target_pair["img"]) 
            embed_msg.set_footer(text="no_pain_no_gain={}".format(no_pain_no_gain))
            await ctx.send(embed=embed_msg)

            response = await wait_for_response(self, ctx, 20)
            
            if response == None:
                await ctx.send("You have 10s left, choose quickly!")
                response = await wait_for_response(self, ctx, 10)

            # verify, then manage the money won / lost here
            valid_responses = { "choice 1":1, "choice 2":2, "choice 3":3, "choice 4":4, "choice 5":5, "1":1, "2":2, "3":3, "4":4, "5":5 }
            if not response in valid_responses:
                line1 = "Invalid response, you lose {} Dodo Dollars!\n".format(bet)
                line2 = "The correct answer was {}, `{}`".format(target_i+1, pairs[target_i]["title"])
                embed_msg = discord.Embed(
                    title="Dodo Club Casino | Image Match Game", 
                    description=line1+line2, 
                    color=0xf27961)
                update_money(db, cur, user_id, -bet)

            elif valid_responses[response] != target_i+1:
                line1 = "Wrong answer, you lose {} Dodo Dollars!\n".format(bet)
                line2 = "The correct answer was {}, `{}`".format(target_i+1, pairs[target_i]["title"])
                embed_msg = discord.Embed(
                    title="Dodo Club Casino | Image Match Game", 
                    description=line1+line2, 
                    color=0xf27961)
                update_money(db, cur, user_id, -bet)
            
            else:
                line1 = "Correct answer, you win {} Dodo Dollars!".format(bet)
                embed_msg = discord.Embed(
                    title="Dodo Club Casino | Image Match Game", 
                    description=line1, 
                    color=0x70febc)
                update_money(db, cur, user_id, bet)
            
            await ctx.send(embed=embed_msg)
            close_db(cur, db)
        
    @image_match.error
    async def image_match_error(self, ctx, error):
        channel = ctx.guild.get_channel(os.environ['CHANNEL'])
        await ctx.send("Syntax for this command is: `,image_match bet <True>`, where \"< >\" denotes an optional parameter.")
        await channel.send(f"{ctx.message.author} experienced a error using image_match. {error}")

# --------------------------------------------------------------------------- #

def setup(client):
    client.add_cog(Games(client))

def test():
    print("testing image_match")
    l = generate_random_images(4, True, True)
    print(str(l))

    # collect 5 random title & img-src pairs. Choose 1 to be the main image.
    pairs = generate_random_images(5, True)
    print(str(pairs))
    target_pair = pairs[random.randint(0, len(pairs)-1)]
    print(str(target_pair))

    # send an embed and wait 30s for answer -> send a followup message when there is only 10s left.
    embed_msg = discord.Embed(title="Dodo Club Casino | Image Match Game", description="Options:", color=0x70febc)
    # TODO: make it so that this is downloaded, then served so that the website can't be easily traced.
    # Or just add a time-limit.
    embed_msg.set_image(url=target_pair["img"]) 
    for (i, pair) in enumerate(pairs):
        embed_msg.add_field(name="*Choice {}*".format(i), value=pair["title"])
    
    print(embed_msg)

# --------------------------------------------------------------------------- #
# Helper Functions: (these do the heavy lifting)

# TODO: option to show the secret words
def generate_random_images(num_images, includes_swears, debug=False):
    word_list = words_20k_includes_swears if includes_swears else words_10k 

    images = None
    width, height = 0, 0
    while images == None:
        # generate random search tokens
        random_words = []
        for _ in range(3):
            random_words.append(random.choice(word_list))

        if debug: print("secret words: {}".format(" ".join(random_words)))

        # NOTE: if google's address convention changes, this will need to be updated
        url = "https://www.google.com/search?q=" + "+".join(random_words) + "&tbm=isch"

        # make an html request & parse the document
        r = requests.get(url)
        if r.status_code != 200:
            if debug: print("Huh, something went wrong. It should work if you try again right away, but if not please let someone know. ^-^")
        soup = BeautifulSoup(r.text, 'html.parser')
    
        images = soup.body.div.next_sibling.next_sibling.table
        if images == None:
            if debug: print("Ooops somthing messed up")
            continue
        elif images.tr == None:
            if debug: print("Ooops, something extra special messed up")
            continue

        height, width = len(images), len(images.tr)
        if width * height < num_images:
            if debug: print("Oops, the secret words were a bit too specific -> TODO try again.")
            images = None

    num_duplicate_captions = 0

    chosen_titles = [] # probably faster than a hashset
    chosen = set()
    choices_list = []
    while len(choices_list) < num_images:
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if debug: print("{} {}".format(x, y))

        identity_str = "{},{}".format(x, y)
        if identity_str in chosen:
            continue
        else:
            messy_pair = list(list(images.children)[y].children)[x]
            stub_head = messy_pair.div.div.div.div.table
            # TODO: write a function which does a http request for the full title of the webpage here, 
            # defaulting to the short one on failure.
            img = stub_head.tr.td.a.div.img.get("src") 
            title = stub_head.tr.next_sibling.td.a.div.span.span.get_text()

            if num_duplicate_captions < num_images and title in chosen_titles:
                num_duplicate_captions += 1
                continue
            
            chosen_titles.append(title)
            chosen.add(identity_str)
            choices_list.append({"img": img, "title": title})
    
    if debug: print("num duplicates: {}".format(num_duplicate_captions))

    return choices_list
