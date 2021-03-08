import discord
import re
import random as rng
import local_settings as ls
# fs = Feng Shui 2 - The Action Movie Role-Playing Game


class action_check:
    def __init__(self, swerve, action_value: int = 0, targets: int = 0, toughness: int = 0, weapon_damage: int = 0, defense: int = 0):
        self.swerve = swerve
        self.action_value = action_value
        self.targets = targets
        self.toughness = toughness
        self.weapon_damage = weapon_damage
        self.defense = defense


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
    if defense:
        arguments["defense"] = int(defense.group(0).split()[1])
    if weapon_damage:
        arguments["weapon_damage"] = int(weapon_damage.group(0).split()[1])
    if toughness:
        arguments["toughness"] = int(toughness.group(0).split()[1])
    return arguments


def attack_args_calulator(arguments, dice_sum):
    """Checks the calculation for each argument in an attack roll, returning result of the most recent 
    complete part of the equation before a 
    missing argument. Assumes Action Value is present (shouldn't be called if it's not). 
    """
    try:
        current_sum = arguments["action_value"] + \
            dice_sum - arguments["targets"]
        result = f" + Action Value of {arguments['action_value']} - {arguments['targets']} for multiple targets = {current_sum}"
    except KeyError
    current_sum = arguments["action_value"] + dice_sum
    result = f" + Action Value of {arguments['action_value']} = {current_sum}"
    try:
        current_sum -= arguments["defense"]
        result += f" - Defense of {arguments['action_value']} = {current_sum}"
    except KeyError:
        return result
    try:
        current_sum += arguments["weapon_damage"]
        result += f" + Weapon Damage of {arguments['weapon_damage']} = {current_sum}"
    except KeyError:
        return result.
    try:
        current_sum -= arguments["toughness"]
        return result += f" - Toughness of {arguments['toughness']} = {current_sum}"
    except KeyError:
        return result


def d6():  # consider making this a more generic die, and the max value being an argument, with optional miniumum=1
    return rng.randint(1, 6)


def explode():
    die = 6
    die_pool = [6]
    while die == 6:
        die = d6()
        die_pool.append(die)
    return die_pool


def fs_roll(arguments):
    """
    Rolls 2d6, subtracting the latter from the former. If both dice are 6, you get Boxcars, and have to roll again.
    If only 1 die is a 6, reroll it until it isn't a 6, adding the results together. Returns rolls and the math thereof.
    Inputs:
        arguments - Expects dictionary from parsed message that ran through fs_argument_parser()
    """
    die1 = d6()
    die2 = d6()
    swerve = {}  # only used if dice explode
    if die1 == 6 and die2 == 6:
        return "boxcars! Roll again. A success will be Way-Awesome, a failure will be Way-Awful!"
    elif die1 < 6 and die2 < 6 and not arguments:
        # Return non-exploding roll if there are no arguments to consider
        return f"[{die1}] - [{die2}] = {die1 - die2}"
    elif die1 == 6:  # If one die explodes, find results, then check for arguments, return if none
        die_pool = explode()
        if not arguments:
            return f"{die_pool} - [{die2}] = {sum(die_pool) - die2}"
        swerve = {"die1": die_pool, "die2": [die2]}
    elif die2 == 6:
        die_pool = explode()
        if not arguments:
            return f"[{die1}] - {die_pool} = {die1 - sum(die_pool)}"
        swerve = {"die1": [die1], "die2": die_pool}
    # If we get here, there are arguments to consider.
    if swerve:  # dice have exploded
        result = f"a swerve of {swerve['die1']} - {swerve['die2']} = {sum(swerve['die1']) - sum(swerve['die2'])}{attack_args_calulator(arguments)}"
        return result
    else:  # dice have not exploded
        result = f"a swerve of [{die1}] - [{die2}] = {die1 - die2}{attack_args_calulator(arguments)"
        return result


def mooks(amount, action_value=8):
    rolls = []
    mook = 0
    try:
        while mook < int(amount):
            die1 = d6()
            if die1 == 6:
                die1 = sum(explode())
            die2 = d6()
            if die2 == 6:
                die2 = sum(explode())
            rolls.append(die1 - die2 + int(action_value))
            mook += 1
        return rolls
    except ValueError:
        return f"Did you send other than numbers? amount = {amount} action_value(optional) = {action_value}"
    except:
        return "Something went wrong. Try again? /mooks <number of rolls> <mook AV(optional)>"


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
    comment = ""
    command = ""
    if '#' in message.content:
        comment = "".join(message.content.split("#")[1:])
        command = message.content[0:message.content.find('#')]
    else:
        command = message.content
    if command.startswith("/fs"):
        # check for arguments made in the message
        args = fs_arg_parser(command)
        reply = f"{user} rolled: {fs_roll(args)}"
        if comment:
            reply += f" {comment}"
        await channel.send(reply)
    elif command.startswith("/init"):
        speed = message.content.split()[1]
        reply = f"{user} rolled a {initiative_roll(int(speed))} for their initiative"
        if comment:
            reply += f" {comment}"
        await channel.send(reply)
    elif command.startswith("/mooks"):
        if len(command) == 3:
            reply = str(mooks(command[1], command[2]))
            if comment:
                reply += f" {comment}"
            await channel.send(reply)
        elif len(command) == 2:
            reply = str(mooks(command[1]))
            if comment:
                reply += f" {comment}"
            await channel.send(reply)
        else:
            await channel.send("Syntax is /mooks <number of rolls> <action_value(optional, default = 8)>")

client.run(ls.token)
