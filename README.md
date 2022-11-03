# whats-on-board

## Description
A simple discord bot that allows you to take and upload photos.
## Use
We use this bot to take photos of our blackboard and upload them to our discord. Therefore, it runs on a Raspberry Pi.

## Installation 
1. Clone the repository
2. Install the dependencies
3. Create a discord bot and add it to your server and generate a token
4. Edit following lines in `discord_bot.py`:
    - `client run option` to your token
    - `discord_object_id` to the discord server ID
5. Optional: Edit the firebase credentials in `firebase.py`

## Run
Run the bot with `python3 main.py`
