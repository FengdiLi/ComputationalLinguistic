#!/usr/bin/env python
import argparse
import re

def main(old_menu, new_menu, category_key, update_key):
    """This main function will read and create two dictionaries 
    representing the category keys and update keys, then check and
    update the price according to its multiplier if the item is 
    associated with a category stated in category keys"""

    new_menu_lines = []

    # add code to read the old menu and look for items with price updates
#########################################################################
    # define a function to check and update the price in a line
    def update(line, keys, cats):
        for key in keys:
                # search item
                if re.search(f'(^|\W){key}($|\W)', line):
                    # retrieve price
                    m = re.match('.*\$(\d+(?:\.\d+)?).*', line)
                    if m:
                        # update and format price
                        price = f'{float(m.group(1))*cats[keys[key]]:.2f}'
                        result = re.sub('\$\d+(\.\d+)?', f'${price}', line)
                        return result
        return line
    
    # initiate category keys
    d = {}
    with open(category_key, 'r') as cat:
        for line in cat:
            line = line.strip().split('\t')
            d[line[0]] = line[1]
    
    # initiate category updates
    d2 = {}
    with open(update_key, 'r') as cat:
        for line in cat:
            line = line.strip().split('\t')
            d2[line[0]] = float(line[1])
    
    # update menu line by line
    with open(old_menu, 'r') as orig_menu:
        for line in orig_menu:
            new_line = update(line, d, d2)
            new_menu_lines.append(new_line)
    
    # write a new file with your updates
    # 'newline' set each ending as LF match the format of example
    with open(new_menu, 'w', newline = '\n') as new_menu_out:
        for line in new_menu_lines:
            new_menu_out.write(line)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update a menu')
    parser.add_argument('--path', type=str, default="practice_menu.txt",
                        help='path to the menu to update')
    parser.add_argument('--output_path', type=str, default="practice_menu_new.txt",
                        help='path to write the updated menu')
    parser.add_argument('--category_key', type=str, default="item_categories.txt",
                        help='path to the key to item categories')
    parser.add_argument('--update_key', type=str, default="category_update.txt",
                        help='path to the key to item categories')


    args = parser.parse_args()
    old_menu = args.path
    new_menu = args.output_path
    category_key = args.category_key
    update_key = args.update_key

    main(old_menu, new_menu, category_key, update_key)
