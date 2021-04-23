<p align=center><img src="kiwi.png" height="200" width="200"></p1>

# SFU Dodo Club - Kiwi
[![discord.py](https://img.shields.io/badge/discord-py-blue.svg)](https://github.com/Rapptz/discord.py)
[![Dodo Club](https://img.shields.io/badge/Dodo-Club-blue.svg)](https://discord.gg/nMCftGkjnC)
[![Paypal Donate](https://img.shields.io/badge/Paypal-Donate-blue.svg)](https://www.paypal.com/paypalme/amandersm)

**Kiwi** is one of SFU Dodo Club's mascots, and is also our main Discord bot. Kiwi is constantly being updated and is maintend by myself. Kiwi is currently being hosted on Heroku and has an MySQL Database connected to it. 

Since Kiwi is changing constantly, it's commands and command parametres are below: 

# Commands
**Kiwi** uses the ``,`` as a prefix. 

## Role Commands
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,collect      | None                 | None                                      | Collect a random role. Command is on a 12 hour cooldown              | ,collect                                 |
| ,activate     | None                 | String text                               | Activate a role that was gained through ``,collect`` as your colour               | ,activate Dodo Red                     |
| ,trade        | None                 | String your_role, @user, String user_role | Trade your role with another user for their role. Other user must accept the trade                           | ,trade Dodo Red @Amander Dodo Purple |
| ,myroles      | None                 | None                                      | Show all of the roles you have collected | ,myroles                                 |
| ,roles        | None                 | None                                      | Show a list of all collectable roles                     | ,roles  
| ,show        | None                 | String role                                      | Display a specific role in your profile tab                     | ,show Dodo red  
| ,showall        | None                 | None                                      | Display all collectable roles in your profile                     | ,showall  
| ,hide        | None                 | String role                                      |Hide a specific role from your profile tab                     | ,hide Dodo Red  
| ,hideall        | None                 | None                                      | Hide all collectable roles in your profile                      | ,hideall  


## Economy
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|                                  
| ,daily        | None                 | None                                      | Recieve your allowance, 24 hour cooldown. Amount recieved is between 1-1000                   | ,daily                                   
| ,bal        | ,balance                 | None                                    | View how much money you have                   | ,bal  
| ,shop        | None                 | None                                      | View shop, and prices for items                    | ,shop                                   
| ,buy        | None                 | int quantity, String role                                    | Buy x of role                   | ,buy 1 Dodo Red  
| ,sell        | None                 | int quantity, String role                                    | Sell x of role, each role can sell between 1-1000                   | ,sell 1 Dodo Red 
| ,leaderboard        | None                 | None                                   | Show top 5 richest users on the server                  | ,leaderboard


## String Manpilation
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,spongebob    | None                 | String text                               | Return the string in "SpOnGeBoB" format                     | ,spongebob Hello World                   |
| ,fireworks    | ,fw                  | String text                               | Return the string with fireworks inbetween the words        | ,fireworks Github is the best            |

## Decision Making

| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,help         | None                 | None                                      | Display a list of all of the commands                       | ,help                                    |
| ,ping         | None                 | None                                      | Returns "pong" if the bot is online                         | ,ping                                    |
| ,poll        | None                | String text String Option 1-10                                     | Give the users to vote on a question. Users can pick from 1-10 responses                             | ,poll "What Movie Should we Watch" Comedy Action "Rom Com"                                          |
| ,_8ball       | ,8ball               | String text                               | Ask Kiwi a Question and get an answer                       | ,8ball Will it snow 


## Astrology
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,horoscope         | ,zodiac                 | String zodiac                                      | Display daily horoscope and compatible matches                     | ,horoscope libra  

## Weather
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,weather         | None                 | String city                                      | Display weather information from requested city                     | ,weather Vancouver  

## Birthday
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,setbirthday         | ,birthday                 | String mmdd                                      | Aadd your birthday in the database so kiwi wishes you a happy birthday                   | ,birthday 0114    


## Other
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,help         | None                 | None                                      | Display a list of all of the commands                       | ,help                                    |
| ,ping         | None                 | None                                      | Returns "pong" if the bot is online                         | ,ping                                                                       
| ,kittyclap    | ,travisclap          | None                                      | Return an emoji of a cat clapping                           | ,kittyclap                               

# Contribute
We welcome changes that benefit the server as a whole! Please feel free to discuss in
our discord server by pinging one of the moderators or post in one of the chats.

# Development Branch
**IMPORTANT** If you are adding a feature to Kiwi, use Dev Branch. After you have pushed your code, head over to the development heroku enviornment, turn on the worker and test your commands in the testing server before merging to main
