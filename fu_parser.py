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

from collections import defaultdict
from glob import iglob
import json
import networkx as nx
import wx

CENTRIFUGE_DATA = 'centrifuge_recipes.config'
DROP_DATA = 'cropharvest.treasurepools.patch'
EXTRACTION_DATA = 'extractionlab_recipes.config'
FU_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU\recipes'
INTERESTING_DROPS = ['ff_resin', 'silk']
SB_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets'
XENO_DATA = 'xenolab_recipes.config'

# DEBUG TEST DATA
TEST_RECIPE = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets\recipes\anvil1\armor\tier1\aviantier1head.recipe'


class FuParser(object):
    def __init__(self):
        self.extractor_recipes = {}
        self.friendly_names = {}
        self.recipes = nx.DiGraph()
        self.unfriendly_names = {}
        self.xeno_recipes = {}

    def parse_centrifuge_data(self):
        # ToDo parse centrifuge data
        pass

    def parse_drop_data(self):
        """Finds interesting drops from the loot tables."""
        # ToDo
        pass

    def parse_extraction_data(self):
        with open(EXTRACTION_DATA, 'r') as extract:
            # ToDo read extraction data
            pass

    def parse_recipes(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('{0}/**/*.recipe'.format(FU_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)
        for recipe_file in iglob('{0}/**/*.recipe'.format(SB_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)

    def parse_xeno_data(self):
        with open(XENO_DATA, 'r') as xeno:
            # ToDo read xeno data
            pass
                    
    def read_friendly_names(self):
        """Reads the more friendly names used within the game from the .item files."""
        # ToDo Can this be refactored to use json module?
        for item_file in iglob('**/*.*item*', recursive=True):
            if '.patch' in item_file:
                continue
            key = item_file.split('\\')[-1].split('.')[0]
            friendly_name = read_friendly_name(item_file)
            self.friendly_names[key] = friendly_name
            self.unfriendly_names[friendly_name] = key
        for item_file in iglob('**/*.object', recursive=True):
            if '.patch' in item_file:
                continue
            key = item_file.split('\\')[-1].split('.')[0]
            friendly_name = read_friendly_name(item_file)
            self.friendly_names[key] = friendly_name
            self.unfriendly_names[friendly_name] = key

        
def filter_description(description):
    """
    Removes color codes from the description and returns the result.
    
    e.g. ^#88e25b;Nuclear Core^white; -> Nuclear Core
         ^red;Arm Cannon -> Arm Cannon
    """
    description = description.strip(';')
    if '^' in description:
        return description.split(';')[1].split('^')[0]
    elif ';' in description:
        return description.split(';')[1]
    else:
        return description


def read_friendly_name(input_file):
    """Reads the 'shortdescription' from the given Starbound file and returns it"""
    # ToDo rewrite to use json module
    with open(input_file, 'r') as item_file:
        for line in item_file:
            if 'shortdescription' in line:
                description = line.split(':')[1].split('"')[1]
                description = filter_description(description)
                return description


def read_recipe(recipe_file):
    # ToDo Should return input materials and output result
    return ((None,), None)


def main():
    parser = FuParser()


if __name__ == '__main__':
    main()
