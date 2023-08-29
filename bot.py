import menu
import os
import discord
import jsonpickle
import json

TOKEN = os.getenv('DISCORD_TOKEN_ROLEPLAY')
client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')


@client.event
async def on_message(message):
    if message.author == client.user or not isinstance(message.channel, discord.channel.DMChannel):
        return
    user_input = message.content
    with open('user_data.json', 'r') as f:
        data = json.load(f)
    if message.author not in data.keys():
        user_menu = menu.MENU()
    else:
        user_menu = jsonpickle.decode(data[message.author], keys=True)
    output = user_menu(user_input)
    data[message.author] = jsonpickle.encode(user_menu, keys=True)
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return output


def run_bot():
    client.run(TOKEN)


if __name__ == "__main__":
    client.run(TOKEN)
