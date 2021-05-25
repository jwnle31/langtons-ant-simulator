# langtons-ant-simulator

This is a Python application that simulates a type of two-dimensional cellular automaton called Langton's Ant.

Classically, this cellular automaton operates under a very simple set of instructions.
1. Ant on ⬜: turns right 90 degrees and moves one unit forward.
2. Ant on ⬛: turns left 90 degrees and moves one unit forward.

More info on Langton's Ant can be found on: https://en.wikipedia.org/wiki/Langton%27s_ant.

However, we can extend this to multiple colors by encoding the rules as a string containing R's and L's.
For each color in order, we can append 'R' or 'L' to the string to assign the colors a left or right turn.
By following this step repeatedly, for the classical rule, we would have the string of 'RL'.

In this program, two extra turns, 'U' and 'N', can be inputted where 'U' is a U-turn and 'N' is a no-turn.
