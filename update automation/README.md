# String and IO Review

This assignment will help reacquaint you with Python strings, regular expressions, and control structures.
Your script must rewrite an input menu, updating certain items' prices based on a multiplier.
The keys that associate items with their categories and categories with their multipliers are in this directory.
For example, the line "milk, $2.49" is category "dairy"; dairy has multiplier 1.05; that works out to 2.6145.
Replace that line with "milk, $2.61".
Use regular expressions carefully to keep all menu formatting, including on lines you don't alter.

Save your solution as menu_update.py. Your code must use the same command line arguments.
Sample input and output is included in this directory for development.
Your script will be graded with a different sample menu and keys in the same, tab-separated format.

Your solution must include:
* string formatting with f-strings
* regular expressions
* safe file I/O
* casting between strings and other types
* a docstring and comments
* an update to this README.md - replace, briefly describing what your code does

The menu_update.py contains the code that read and create two dictionaries representing the category keys ('item_categories.txt') and update keys ('category_update.txt'), 
then check and update the price in each line of the old menu ('practice_menu.txt') according to its multiplier if this item is associated with a category stated in category keys, 
and finally save the new menu to a text file named 'practice_menu_new.txt'.