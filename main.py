from game import GAME
from menu import MENU
from adventure import ADVENTURE

import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN_ROLEPLAY')
client = discord.Client(intents=discord.Intents.default())
menus = {}
options = {}


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')


@client.event
async def on_message(message):
    global menus
    if message.author == client.user or not isinstance(message.channel, discord.channel.DMChannel):
        return
    username = message.author.name
    if username not in menus.keys():
        menus.update({username: MENU(options)})
    answer = menus[username].call(message.content)
    await message.channel.send(answer)

if __name__ == '__main__':
    # global options
    adv1 = ADVENTURE()
    adv2 = ADVENTURE()
    options = {'adventure1': adv1.play, 'adventure2': adv2.play}
    client.run(TOKEN)


# maybe single documents for each of these bigger classes
# think about OpenAI-API connections
# think about general use of AI
# think about how to save data
# think about multiplayer


'''
The game basically consists of 
    the player trying to find secrets searching his location and speaking with the npcs.
    Changing locations
    triggers
    At some point: fighting monsters and npcs.
'''