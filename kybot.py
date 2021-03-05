import discord
import re
import random as rng

# fs = Feng Shui 2 - The Action Movie Role-Playing Game


def fs_arg_parser(args_list):
    """returns a dictionary of arguments for fs_roll() to use"""
    action_value = re.search(r"\s[-][a|A][v|V]\s\d+", args_list)
    targets = re.search(r"\s[-][t|T]\s\d+", args_list)
    toughness = re.search(r"\s[-][t|T][o|O][u|U]\s\d+", args_list)
    weapon_damage = re.search(r"\s[-][w|W]\s\d+", args_list)
    defense = re.search(r"\s[-][d|D]\s\d+", args_list)
    arguments = {}
    if action_value:
        arguments["action_value"] = int(action_value.group(0).split()[1])
    if targets:
        arguments["targets"] = int(targets.group(0).split()[1])
    if toughness:
        arguments["toughness"] = int(toughness.group(0).split()[1])
    if weapon_damage:
        arguments["weapon_damage"] = int(weapon_damage.group(0).split()[1])
    if defense:
        arguments["defense"] = int(defense.group(0).split()[1])
    return arguments


def d6():
    return rng.randint(1, 6)


def fs_roll():
    """
    Rolls 2d6, subtracting the latter from the former. If both dice are 6, you get Boxcars, and have to roll again.
    If only 1 die is a 6, reroll it until it isn't a 6, adding the results together. Returns rolls and the math thereof.
    """
    die1 = d6()
    die2 = d6()
    if die1 == 6 and die2 == 6:
        return "boxcars! Roll again. A success will be Way-Awesome, a failure will be Way-Awful!"
    elif die1 < 6 and die2 < 6:
        return f"[{die1}] - [{die2}] = {die1 - die2}"
    elif die1 == 6:
        die_pool = []
        die_pool.append(die1)
        while die1 == 6:
            die1 = d6()
            die_pool.append(die1)
        return f"{die_pool} - [{die2}] = {sum(die_pool) - die2}"
    elif die2 == 6:
        die_pool = []
        die_pool.append(die2)
        while die2 == 6:
            die2 = d6()
            die_pool.append(die1)
        return f"[{die1}] - {die_pool} = {die1 - sum(die_pool)}"
    return f"Something didn't work and we got there die1: {die1} die2: {die2}"


def initiative_roll(speed):
    """Rolls a d6 and adds the input speed value of the character (input from Discord command)"""
    if type(speed) != int:
        return f"Format for Initiative is `/init <intiger>` (your speed value was '{speed}')"
    die = d6()
    return f"rolled [{die}] + {speed} = {die+speed}"


client = discord.Client()


@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("/fs to roll"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    user = message.author
    if message.content.startswith("/fs"):
        await channel.send(f"{user} rolled: fs_roll()")
    elif message.content.startswith("/init"):
        speed = message.content.split()[1]
        await channel.send(f"{user} rolled a {initiative_roll(int(speed))} for their initiative")
