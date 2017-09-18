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
import networkx as nx
import wx

DROP_DATA = 'cropharvest.treasurepools.patch'
EXTRACTION_DATA = 'extractionlab.lua'
INTERESTING_DROPS = ['ff_resin', 'silk']
X_MODIFIER = 3
X_OFFSET = 1
XENO_DATA = 'xenolab.lua'
Y_MODIFIER = 3


class FuParser(object):
    def __init__(self):
        self.extractor_recipes = {}
        self.extractor_sources = defaultdict(list)
        self.friendly_names = {}
        self.interesting_drops = defaultdict(list)
        self.recipes = nx.DiGraph()
        self.unfriendly_names = {}
        self.xeno_recipes = {}
        self.xeno_sources = defaultdict(list)
        
    def parse_craftables(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('**/*.recipe', recursive=True):
            pass
        
    def parse_drop_data(self):
        """Finds interesting drops from the loot tables."""
        # ToDo
        pass

    def parse_extraction_data(self):
        with open(EXTRACTION_DATA, 'r') as extract:
            pass
    
    def parse_xeno_data(self):
        with open(XENO_DATA, 'r') as xeno:
            pass
                    
    def read_friendly_names(self):
        """Reads the more friendly names used within the game from the .item files."""
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
    with open(input_file, 'r') as item_file:
        for line in item_file:
            if 'shortdescription' in line:
                description = line.split(':')[1].split('"')[1]
                description = filter_description(description)
                return description


def main():
    parser = FuParser()


if __name__ == '__main__':
    main()
