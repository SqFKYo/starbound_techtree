#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright 2016 SqFKYo
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from glob import iglob
import json
import networkx as nx
import os
import wx

# Not yet used
CENTRIFUGE_DATA = 'centrifuge_recipes.config'
DROP_DATA = 'cropharvest.treasurepools.patch'
EXTRACTION_DATA = 'extractionlab_recipes.config'
FRIENDLY_NAMES = 'friendly_names.csv'
INTERESTING_DROPS = ['ff_resin', 'silk']
XENO_DATA = 'xenolab_recipes.config'

# Currently in use
FU_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU'
SB_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets'


class SbParser(object):
    def __init__(self):
        self.extractor_recipes = {}
        self.friendly_names = {}
        self.crafting_recipes = nx.DiGraph()
        self.unfriendly_names = {}
        self.xeno_recipes = {}

    def parse_biome_data(self):
        # ToDo read biome data to determine where to get raw ingredients biomes\**\.biome and patch files
        pass

    def parse_centrifuge_data(self):
        # ToDo parse centrifuge data
        pass

    def parse_crafting_recipes(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(FU_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.crafting_recipes.add_edge(material, result)
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(SB_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.crafting_recipes.add_edge(material, result)

    def parse_drop_data(self):
        """Finds interesting drops from the loot tables."""
        # ToDo read treasure drop data treasure\cropharvest.treasurepools(.patch)
        pass

    def parse_extraction_data(self):
        with open(EXTRACTION_DATA, 'r') as extract:
            # ToDo read extraction data
            pass

    def parse_xeno_data(self):
        with open(XENO_DATA, 'r') as xeno:
            # ToDo read xeno data
            pass
                    
    def read_friendly_names(self):
        """Reads the more friendly names used within the game from the previously created file."""
        with open(FRIENDLY_NAMES, 'r') as f:
            pass
        raise NotImplementedError


def dump_friendly_names(dump_file):
    """Reads the friendly names used within the game from the item and object folders and dumps them into a file."""
    # ToDo Can read_friendly_names be refactored to use json module?
    ARMORS = ['.back', '.chest', '.head', '.legs']
    SKIPPABLES = ['.activeitem', '.animation', '.combofinisher', '.config', '.frames', '.inspectiontool',
                  '.lua', '.patch', '.png', '.unlock', '.weaponability', '.weaponcolors']
    friendly_names = {}
    unfriendly_names = {}
    for item_file in iglob('{0}/items/**/*.*'.format(SB_PATH), recursive=True):
        if any([to_skip in item_file for to_skip in SKIPPABLES]):
            continue
        with open(item_file, 'r') as f:
            try:
                loaded_file = json.load(f)
                friendly_name = loaded_file['shortdescription']
                unfriendly_name = loaded_file['itemName']
                friendly_names[unfriendly_name] = friendly_name
                unfriendly_names[friendly_name] = unfriendly_name
            except json.decoder.JSONDecodeError:
                if any([armor in item_file for armor in ARMORS]):
                    with open(item_file, 'r') as f:
                        read_file = f.readlines()
                        friendly_line = next(line for line in read_file if 'shortdescription' in line)
                        friendly_name = friendly_line.split(':')[1].strip().strip('",')
                        unfriendly_line = next(line for line in read_file if 'itemName' in line)
                        unfriendly_name = unfriendly_line.split(':')[1].strip().strip('",')
                        friendly_names[unfriendly_name] = friendly_name
                        unfriendly_names[friendly_name] = unfriendly_name
                else:
                    print(item_file)
            except KeyError:
                print(item_file)
    for item_file in iglob('{0}/objects/**/*.*'.format(SB_PATH), recursive=True):
        pass
    # ToDo ditto for objects folder and FU folders
    print('apextier1chest' in friendly_names)
    print("Defector's Chestguard" in unfriendly_names)
    raise NotImplementedError


def filter_description(description):
    """
    Removes color codes from the description and returns the result.
    
    e.g. ^#88e25b;Nuclear Core^white; -> Nuclear Core
         ^red;Arm Cannon -> Arm Cannon
    """
    # ToDo feature for filter_description
    description = description.strip(';')
    if '^' in description:
        return description.split(';')[1].split('^')[0]
    elif ';' in description:
        return description.split(';')[1]
    else:
        return description


def read_recipe(recipe_file):
    """Reads recipe json file and returns inputs and the output as tuple of generator exp and string"""
    with open(recipe_file, 'r') as f:
        loaded_file = json.load(f)
        output = loaded_file['output']['item']
        inputs = (x['item'] for x in loaded_file['input'])
    return (inputs, output)


def main():
    parser = SbParser()
    parser.read_friendly_names()
    parser.parse_crafting_recipes()
    parser.parse_centrifuge_data()
    parser.parse_extraction_data()
    parser.parse_xeno_data()
    parser.parse_drop_data()
    parser.parse_biome_data()

if __name__ == '__main__':
    dump_friendly_names(None)
    main()
