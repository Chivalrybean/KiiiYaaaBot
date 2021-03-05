import discord
import re
import random as rng

# fs = Feng Shui 2 - The Action Movie Role-Playing Game


def d6_exploding():
    die = rng.randint(1, 6)
    result = die
    while die == 6:
        die = rng.randint(1, 6)
        result = result + die
    return result


def fs_roll():
    result = d6_exploding() - d6_exploding()
    return result


client = discord.Client()


@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("&island to create invite"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("/fs"):
        channel = message.channel
        user = message.author
