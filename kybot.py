import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
import re
import random as rng
import local_settings as ls
import asyncio
# fs = Feng Shui 2 - The Action Movie Role-Playing Game

class Swerve:
    def __init__(self, die1, die2):
        self.die1 = die1
        self.die2 = die2
        self.total = sum(self.die1) - sum(self.die2)

    def get_total(self):
        return self.total
        
    def __repr__(self):
        f"{self.die1} - {self.die2} = {self.total}"

class Action_check:
    def __init__(self, swerve, action_value, targets, defense, weapon_damage, toughness):
        self.swerve = swerve
        self.action_value = action_value
        self.targets = targets
        self.defense = defense
        self.weapon_damage = weapon_damage
        self.toughness = toughness
        self.result = self.generate_result()
    # When checking the various arguments, I don't need to do else statements, only ifs!
    def generate_result(self):
        response = f"{swerve}"
        current_total = swerve.get_total()
        if self.action_value is not None:
            current_total += self.action_value
            response += f" + Action Value of {self.action_value}"
            if self.targets is not None:
                current_total -= self.targets
                response += f" - {self.targets} for multiple targets"
            if self.defense is not None:
                current_total -= self.defense
                response += f" - defense of {self.defense}"
                if current_total < 0:
                    response += f" = {current_total}, which is a miss."
                    if self.comment is not None:
                        response += f" {self.comment}"
                    return response
                if self.weapon_damage is not None:
                    current_total += self.weapon_damage
                    response += f" + weapon damage of {self.weapon_damage}"
                    if self.toughness is not None:
                        current_total -= self.toughness
                        response += f" - toughness of {self.toughness}"
            if self.comment is not None:
                response += f". {self.comment}"
        else:
            if self.comment is not None:
                response =+ f" = {current_total}. {self.comment}"
            else:
                response += f" = {current_total}."
        return response
    def __repr__(self):
        self.result()

def swerve_roller(die1, die2):
    while die1 !=6 and die2 != 6:
        die1 = d6()
        die2 = d6()
    if die1 == 6:
        die1, die2 = explode(), [die2]
    elif die2 == 6:
        die1, die2 = [die1], explode()
    else:
        die1, die2 = [die1], [die2]
    return Swerve(die1, die2)

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
    missing argument.
    """
    try:
        current_sum = arguments["action_value"] + \
            dice_sum - arguments["targets"]
        result = f" + Action Value of {arguments['action_value']} - {arguments['targets']} for multiple targets = {current_sum}"
    except KeyError:
        try:
            current_sum = arguments["action_value"] + dice_sum
            result = f" + Action Value of {arguments['action_value']} = {current_sum}"
        except KeyError:
            result = ". No Action Value `-av <digits>` supplied. Calculation prevented"
            return result
    try:
        current_sum -= arguments["defense"]
        if current_sum < 0:
            result += f" - Defense of {arguments['defense']} = {current_sum} which is a miss"
            return result
        result += f" - Defense of {arguments['defense']} = {current_sum}"
    except KeyError:
        return result
    try:
        current_sum += arguments["weapon_damage"]
        result += f" + Weapon Damage of {arguments['weapon_damage']} = {current_sum}"
    except KeyError:
        return result
    try:
        current_sum -= arguments["toughness"]
        result += f" - Toughness of {arguments['toughness']} = {current_sum}"
        return result
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
        dice_sum = sum(swerve['die1']) - sum(swerve['die2'])
        result = f"a swerve of {swerve['die1']} - {swerve['die2']} = {dice_sum}{attack_args_calulator(arguments, dice_sum)}"
        return result
    else:  # dice have not exploded
        dice_sum = die1 - die2
        result = f"a swerve of [{die1}] - [{die2}] = {dice_sum}{attack_args_calulator(arguments, dice_sum)}"
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


guild_ids = [701612732062892153, 351522944461307915]

client = commands.Bot(command_prefix="/")
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("/fs to roll"))

fs_options = [
    {
        "name": "action_value",
        "description": "Include the character's Action Value to the roll",
        "required": False,
        "type": 4
    },
    {
        "name": "targets",
        "description": "How many targets are you trying to hit?",
        "required": False,
        "type": 4
    },
    {
        "name": "defense",
        "description": "The defense of the target (highest one of multiple targets). Will note miss and stop if < 0",
        "required": False,
        "type": 4
    },
    {
        "name": "weapon_damage",
        "description": "Include the character's Action Value to the roll",
        "required": False,
        "type": 4
    },
    {
        "name": "toughness",
        "description": "Toughness of the target.",
        "required": False,
        "type": 4
    },
    {
        "name": "comment",
        "description": "Something to append onto the end of the roll.",
        "required": False,
        "type": 4
    }
]


def append_comment(comment):
    if comment is not None:
        return f". {comment}"
    else:
        return "."


@slash.slash(name="fs", description="Outputs standard open roll for Feng Shui 2", options=fs_options, guild_ids=guild_ids)
async def _fs(ctx, action_value=None, targets=None, defense=None, weapon_damage=None, toughness=None, comment=None):
    """Add in the default inputs, AV, etc. Completely rework handling the arguments here."""
    await ctx.respond()
    channel = ctx.message.channel
    user = ctx.message.author
    # This is there the changes must begin
    die1 = d6()
    die2 = d6()
    if die1 == 6 and die2 == 6:
        channel.send("{user} rolled Boxcars! Rerolling for a Way-Awesome Success, or Way-Awful Failure!")
        reroll = channel.send("rerolling ...")
        asyncio.sleep(3)
        response = Action_check(swerve_roller(die1, die2), action_value, targets, defense, weapon_damage, toughness)
        reroll.edit(f"{user} rolled {response}")
    else:
        response = Action_check(swerve_roller(die1, die2), action_value, targets, defense, weapon_damage, toughness)
        reroll.edit(f"{user} rolled {response}")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     channel = message.channel
#     user = message.author
#     comment = ""
#     command = ""
#     if '#' in message.content:
#         comment = "".join(message.content.split("#")[1:])
#         command = message.content[0:message.content.find('#')]
#     else:
#         command = message.content
#     if command.startswith("/fs"):
#         # check for arguments made in the message
#         args = fs_arg_parser(command)
#         reply = f"{user} rolled: {fs_roll(args)}."
#         if comment:
#             reply += f" {comment}"
#         await channel.send(reply)
#     elif command.startswith("/init"):
#         try:
#             speed = message.content.split()[1]
#             reply = f"{user} rolled a {initiative_roll(int(speed))} for their initiative."
#         except IndexError or ValueError:
#             await channel.send("Initiative syntax is `/init <Speed(must be digits)>`")
#             return
#         if comment:
#             reply += f" {comment}"
#         await channel.send(reply)
#     elif command.startswith("/mooks"):
#         command = command.split()
#         if len(command) == 3:
#             reply = str(mooks(command[1], command[2]))
#             if comment:
#                 reply += f" {comment}"
#             await channel.send(reply)
#         elif len(command) == 2:
#             reply = str(mooks(command[1]))
#             if comment:
#                 reply += f" {comment}"
#             await channel.send(reply)
#         else:
#             await channel.send("Syntax is /mooks <number of rolls> <action_value(optional, default = 8)>")

client.run(ls.token)
