<p align=center><img src="kiwi.png" height="200" width="200"></p1>

# SFU Dodo Club - Kiwi
[![discord.py](https://img.shields.io/badge/discord-py-blue.svg)](https://github.com/Rapptz/discord.py)
[![Dodo Club](https://img.shields.io/badge/discord-blue.svg)](https://discord.gg/nMCftGkjnC)

**Kiwi** is one of SFU Dodo Club's mascots, and is also our main Discord bot. Kiwi is constantly being updated and is maintend by myself. Kiwi is currently being hosted on Heroku and has an MySQL Database connected to it. 

Some of the bot's ability is maniuplate a user's input in different ways, give responses based on a question, flip a coin, allow users to collect and trade roles. 

# Commands
**Kiwi** uses the ``,`` as a prefix. 

## Role Commands
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,collect      | None                 | None                                      | Collect a random colour role, 12 hour cooldown              | ,collect                                 |
| ,activate     | None                 | String text                               | Activate a collect colour role as your colour               | ,activate "Dodo Red"                     |
| ,trade        | None                 | String your_role, @user, String user_role | Trade your role with another user                           | ,trade "Dodo Red" @Amander "Dodo Purple" |
| ,myroles      | None                 | None                                      | Display a list and quantity of the roles you have collected | ,myroles                                 |
| ,roles        | None                 | None                                      | Display a list of all collectable roles                     | ,roles                                   

## Economy
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|                                  
| ,daily        | None                 | None                                      | Recieve your allowance, 24 hour cooldown                    | ,daily                                   
| ,bal        | ,balance                 | None                                    | View how much money you have                   | ,bal  

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





## Other
| Command       | Alias                | Parameters                                | Description                                                 | Example                                  |
|---------------|----------------------|-------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| ,help         | None                 | None                                      | Display a list of all of the commands                       | ,help                                    |
| ,ping         | None                 | None                                      | Returns "pong" if the bot is online                         | ,ping                                                                       
| ,kittyclap    | ,travisclap          | None                                      | Return an emoji of a cat clapping                           | ,kittyclap                               

# Contribute
We welcome changes that benefit the server as a whole! Please feel free to discuss in
our discord server by pinging one of the moderators or post in one of the chats.

