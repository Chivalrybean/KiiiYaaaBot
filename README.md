# KiiiYaaaBot

Discord bot to assist in playing Feng Shui 2

\*First up
(COMPLETED)Set up regular die roller for FS2
/fs
1d6-1d6, 6s explode.
Checks for Boxcars

Make /fs <number> work without -argument tag. 

Add ability to add string after # for output with die roll

Set up arguments for /fs
-a <number> Add action value
-d <number> Target's defense value
-t <number> Targets, ignore if less than 2. Reduces action value by number.

Program reponses to hits, for input of weapon and toughness values, generating a final damage.

\*Later
Shot Counter initiative tracking, and character objects that track wound points, taking action will roll, spend shots, etc. with prompts for adjustments to normal costs (timeout = typical costs)

BUGS
/init (without number) fails without error or message about proper syntax