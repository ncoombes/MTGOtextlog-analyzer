# MTGOtextlog-analyzer
A utility for reading in magic online text logs for data analysis

Magic online has a text log that is pretty (but not completely) descriptive of what occured during a game of magic. For example here is a slice of a game:

11:35 PM: Turn 1: player A
11:35 PM: player A skips their draw step.
11:35 PM: player A plays Simic Guildgate.
11:35 PM: Turn 1: player B
11:35 PM: player B plays Forest.
11:35 PM: Turn 2: player A
11:35 PM: player A plays Gruul Guildgate.
11:35 PM: player A casts Pteramander.
11:35 PM: Turn 2: player B
11:35 PM: player B plays Gateway Plaza.
11:35 PM: player B puts triggered ability from Gateway Plaza onto the stack (When Gateway Plaza enters the battlefield, sacrifice it unless you pay  .).

This repository includes functions intended to parse these text strings and generate data structures that can be more easily analyzed using data analysis.
