# import discord
# from discord.ext import commands
# from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext

from interactions import slash_command, SlashContext, Client
import random as rng
import local_settings as ls
import asyncio
from xcard import xcard
# fs = Feng Shui 2 - The Action Movie Role-Playing Game


class Swerve:
    def __init__(self, die1, die2):
        self.die1 = die1
        self.die2 = die2
        self.total = sum(die1) - sum(die2)

    def get_total(self):
        return self.total

    def __repr__(self):
        return f"{self.die1} - {self.die2} = **{self.total}**"


class Action_check:
    def __init__(self, swerve, action_value, targets, defense, weapon_damage, toughness, comment):
        self.swerve = swerve
        self.action_value = action_value
        self.targets = targets
        self.defense = defense
        self.weapon_damage = weapon_damage
        self.toughness = toughness
        self.comment = comment
        self.result = self.generate_result()
    # When checking the various arguments, I don't need to do else statements, only ifs!

    def generate_result(self):
        response = f"{self.swerve}"
        current_total = self.swerve.get_total()
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
                    response += f" = **{current_total}**, which is a miss."
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
                response += f" = **{current_total}**. {self.comment}"
            else:
                response += f" = **{current_total}**."
        else:
            if self.comment is not None:
                response += f". {self.comment}"
        return response

    def __repr__(self):
        return self.result


def swerve_roller(die1, die2):
    while die1 == 6 and die2 == 6:
        die1 = d6()
        die2 = d6()
    if die1 == 6:
        die1, die2 = explode(), [die2]
    elif die2 == 6:
        die1, die2 = [die1], explode()
    else:
        die1, die2 = [die1], [die2]
    return Swerve(die1, die2)


def d6():  # consider making this a more generic die, and the max value being an argument, with optional miniumum=1
    return rng.randint(1, 6)


def explode():
    die = 6
    die_pool = [6]
    while die == 6:
        die = d6()
        die_pool.append(die)
    return die_pool


def mooks(amount, action_value=8):
    rolls = []
    mook = 0
    try:
        while mook < amount:
            die1 = d6()
            if die1 == 6:
                die1 = sum(explode())
            die2 = d6()
            if die2 == 6:
                die2 = sum(explode())
            rolls.append(die1 - die2 + action_value)
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


guild_ids = [701612732062892153, 351522944461307915, 881989509812715530, 442268525835452416, 218111230433427456]

client = Client(command_prefix="/")
# slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))
    await client.change_presence(status=client.Status.idle, activity=client.Game("/fs to roll"))

fs_options = [
    {
        "name": "action_value",
        "description": "Include the character's Action Value to the roll",
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
        "type": 3
    },
    {
        "name": "targets",
        "description": "How many targets are you trying to hit?",
        "required": False,
        "type": 4
    }
]


@slash_command(name="fs", description="Outputs standard open roll for Feng Shui 2", options=fs_options, scopes=guild_ids)
async def _fs(ctx: SlashContext, action_value=None,  defense=None, weapon_damage=None, toughness=None, targets=None, comment=None):
    """Add in the default inputs, AV, etc. Completely rework handling the arguments here."""
    # await ctx.respond()
    # channel = ctx.channel
    user = ctx.author
    die1 = d6()
    die2 = d6()
    if die1 == 6 and die2 == 6:
        await ctx.send(f"<@{user.id}> rolled Boxcars[6][6]! Rerolling for a Way-Awesome Success, or Way-Awful Failure!")
        await asyncio.sleep(3)
        reroll = await ctx.send("rerolling ...")
        await asyncio.sleep(3)
        response = Action_check(swerve_roller(
            die1, die2), action_value, targets, defense, weapon_damage, toughness, comment)
        await reroll.edit(content=f"<@{user.id}> rolled {response}")
    else:
        response = Action_check(swerve_roller(
            die1, die2), action_value, targets, defense, weapon_damage, toughness, comment)
        await ctx.send(f"<@{user.id}> rolled {response}")

mook_options = [
    {
        "name": "amount",
        "description": "How many times to roll? (default is 1)",
        "required": False,
        "type": 4
    },
    {
        "name": "action_value",
        "description": "Adjust the standard AV of 8",
        "required": False,
        "type": 4
    }
]


@slash_command(name="mooks", description="Roll some mook rolls!", options=mook_options, scopes=guild_ids)
async def _mooks(ctx: SlashContext, amount=1, action_value=8):
    # await ctx.respond()
    # channel = ctx.channel
    await ctx.send(f"{mooks(amount, action_value)}")


init_options = [
    {
        "name": "speed",
        "description": "The speed value of your character",
        "required": True,
        "type": 4
    }
]


@slash_command(name="init", description="Roll for initiative (Feng Shui 2)!", options=init_options, scopes=guild_ids)
async def _mooks(ctx: SlashContext, speed):
    # await ctx.respond()
    # channel = ctx.channel
    user = ctx.author
    await ctx.send(
        f"<@{user.id}> rolled {initiative_roll(speed)} for initiative.")

xcard_options = [
    {
        "name": "verify",
        "description": "Type True if you're using this for intended purpose. Don't use as a joke.",
        "required": True,
        "type": 5
    },
    {
        "name": "reason",
        "description": "If you wish, you can provide a reason, it is not required.",
        "required": False,
        "type": 3
    }
]


@slash_command(name="d6", description="Roll a six-sided die, for fortune, or other abilities", scopes=guild_ids)
async def _d6(ctx: SlashContext):
    # await ctx.respond()
    # channel = ctx.channel
    user = ctx.author
    await ctx.send(f"<@{user.id}> rolled a {d6()}.")


@slash_command(name="xcard", description="Request a pause in RPG game to redirect away from something.", scopes=guild_ids, options=xcard_options)
async def _xcard(ctx, verify=False, reason="No specifics given"):
    # await ctx.respond()
    # channel = ctx.channel
    user = ctx.author
    await ctx.send(f"<@{user.id}> placed an X Card on the table\n{xcard}\nReason: {reason}")


client.start(ls.token)
