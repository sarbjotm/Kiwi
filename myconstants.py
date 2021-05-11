# Holds all the constants that we want to be consistent

#TODO: change these all to snake case

rolesList = ['Dodo Red', 'Dodo Orange', 'Dodo Yellow', 'Dodo Spring', 'Dodo Matcha', 'Dodo Mint', 'Dodo Green',
             'Dodo Ice', 'Dodo Bbblu', 'Dodo Teal', 'Dodo Copyright', 'Dodo Cyan', 'Dodo Blue', 'Dodo Lavender',
             'Dodo Grape', 'Dodo Purple', 'Dodo Rose', 'Dodo Pink', 'Dodo Salmon', 'Dodo Special', 'Dodo Taffy',
             'Dodo Oak', 'Dodo Snow', 'Dodo Black', 'Dodo Gold', 'Dodo Dream']

activateRoles = ['Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Copyright', 'Cyan', 'Blue', 'Grape', 'Purple', 'Rose',
                 'Pink', 'Salmon', 'Spring', 'Matcha', 'Mint', 'Ice', 'Bbblu', 'Lavender', 'Special', 'Taffy', 'Oak',
                 'Snow', 'Black', 'Gold', 'Dream']

numbers = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
suits = ["🍇", "🍉", "🍒", "🍍"]

# Each sign is referenced to a number assigned by horoscope.com, this goes to the end of sign =
zodiacSigns = {
    "aries": "1",
    "taurus": "2",
    "gemini": "3",
    "cancer": "4",
    "leo": "5",
    "virgo": "6",
    "libra": "7",
    "scorpio": "8",
    "sagittarius": "9",
    "capricorn": "10",
    "aquarius": "11",
    "pisces": "12"
}

zodiacAvatars = ["", "https://www.horoscope.com/images-US/signs/profile-aries.png",
                 "https://www.horoscope.com/images-US/signs/profile-taurus.png",
                 "https://www.horoscope.com/images-US/signs/profile-gemini.png",
                 "https://www.horoscope.com/images-US/signs/profile-cancer.png",
                 "https://www.horoscope.com/images-US/signs/profile-leo.png",
                 "https://www.horoscope.com/images-US/signs/profile-virgo.png",
                 "https://www.horoscope.com/images-US/signs/profile-libra.png",
                 "https://www.horoscope.com/images-US/signs/profile-scorpio.png",
                 "https://www.horoscope.com/images-US/signs/profile-sagittarius.png",
                 "https://www.horoscope.com/images-US/signs/profile-capricorn.png",
                 "https://www.horoscope.com/images-US/signs/profile-aquarius.png",
                 "https://www.horoscope.com/images-US/signs/profile-pisces.png"]

pollOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

weather_table = {
    "clouds"  : "http://getdrawings.com/free-icon/cloudy-icon-62.png",

    "clear"   : "https://cdn3.iconfinder.com/data/icons/summertime-1/44/summertime-03-512.png", 
    "sun"     : "https://cdn3.iconfinder.com/data/icons/summertime-1/44/summertime-03-512.png", 
    "sunny"   : "https://cdn3.iconfinder.com/data/icons/summertime-1/44/summertime-03-512.png",

    "snow"    : "https://www.freeiconspng.com/thumbs/snow-icon/blue-snow-icon-8.png",

    "rain"    : "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather07-512.png",
    "showers" : "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather07-512.png",

    "default" : "https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/63069/weather-icon-clipart-md.png"
}

# --------------------------------------------------------------------------- #

def load_data():
    global words_10k, words_20k_includes_swears
    with open("./data/google-10k-english-no-swears.txt", "r") as f:
        words_10k = [x.strip() for x in f.readlines()]
            
    with open("./data/20k.txt", "r") as f:
        words_20k_includes_swears = [x.strip() for x in f.readlines()]

    import random

# --------------------------------------------------------------------------- #
# variables under here must be filled using load_data()

words_10k = []
words_20k_includes_swears = [] 