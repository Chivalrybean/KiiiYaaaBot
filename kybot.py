import discord
import re
import random as rng

# fs = Feng Shui 2 - The Action Movie Role-Playing Game


def d6():
    return rng.randint(1, 6)


def fs_roll():
    die1 = d6()
    die2 = d6()
    if die1 == 6 and die2 == 6:
        return "Boxcars! Roll again. A success will be Way-Awesome, a failure will be Way-Awful!"
    elif die1 < 6 and die2 < 6:
        return f"[{die1}] - [{die2}] = {die1 - die2}"
    elif die1 == 6:
        die_pool = []
        die_pool.append(die1)
        while die1 == 6:
            die1 = d6()
            die_pool.append(die1)
        return f"[{die_pool}] - [{die2}] = {sum(die_pool) - die2}"
    elif die2 == 6:
        die_pool = []
        die_pool.append(die2)
        while die2 == 6:
            die2 = d6()
            die_pool.append(die1)
        return f"[{die1}] - [{die_pool}] = {die1 - sum(die_pool)}"
    return f"Something didn't work and we got there die1: {die1} die2: {die2}"


client = discord.Client()


@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("/fs to roll"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("/fs"):
        channel = message.channel
        user = message.author
        await channel.send(f"{user} rolled: fs_roll()")
