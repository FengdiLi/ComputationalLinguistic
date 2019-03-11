# String and IO Review

This assignment will help reacquaint you with Python strings, regular expressions, and control structures.
Your script must rewrite an input menu, updating certain items' prices based on a multiplier.
The keys that associate items with their categories and categories with their multipliers are in this directory.
For example, the line "milk, $2.49" is category "dairy"; dairy has multiplier 1.05; that works out to 2.6145.
Replace that line with "milk, $2.61".

The `menu_update.py` contains the code that read and create two dictionaries representing the category keys (`item_categories.txt`) and update keys (`category_update.txt`), 
then check and update the price in each line of the old menu (`practice_menu.txt`) according to its multiplier if this item is associated with a category stated in category keys, 
and finally save the new menu to a text file named `practice_menu_new.txt`.
