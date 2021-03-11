# KiiiYaaaBot

Discord bot to assist in playing Feng Shui 2

\*First up
(COMPLETED)Set up regular die roller for FS2
/fs (completed)
1d6-1d6, 6s explode. (completed)
Checks for Boxcars (completed)

Make /fs <number> work without -argument tag. (completed by implimenting Discord Slash Command functionality)

Add ability to add string after # for output with die roll (Completed, but will be swapped for Slash Command function.)
Might actually not need Comment as Slash Command input, user can just type in text field normally. Must investigate.

Set up arguments for /fs (completed - Uses Slash Command now not --arguments)
-a <number> Add action value
-d <number> Target's defense value
-t <number> Targets, ignore if less than 2. Reduces action value by number.

Program reponses to hits, for input of weapon and toughness values, generating a final damage. (maybe don't need this)

(Completed)Set up /mooks <amount> -av(optional) to generate a number of mook attacks, optionally with something outside the default action value

\*Later
Shot Counter initiative tracking, and character objects that track wound points, taking action will roll, spend shots, etc. with prompts for adjustments to normal costs (timeout = typical costs)

BUGS
