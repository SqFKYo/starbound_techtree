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
from itertools import chain
import json
import networkx as nx
import wx

# Not yet used
DROP_DATA_FU = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU\treasure\cropharvest.treasurepools.patch'
DROP_DATA_SB = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets\treasure\cropharvest.treasurepools'
INTERESTING_DROPS = ['ff_resin', 'silk']

# Currently in use
CENTRIFUGE_DATA = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU\objects\generic\centrifuge_recipes.config'
EXTRACTION_DATA = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU\objects\generic\extractionlab_recipes.config'
FRIENDLY_NAMES = 'friendly_names.csv'
FU_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU'
SB_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets'
XENO_DATA = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU\objects\generic\xenostation_recipes.config'


class SbParser(object):
    def __init__(self):
        self.biome_data = {}
        self.centrifuge_data = {}
        self.extractor_data = {}
        self.friendly_names = {}
        self.recipes = nx.DiGraph()
        self.unfriendly_names = {}
        self.xeno_data = {}

    def parse_biome_data(self):
        # ToDo read biome data to determine where to get raw ingredients biomes\**\.biome and patch files
        pass

    def parse_centrifuge_data(self):
        with open(CENTRIFUGE_DATA, 'r') as f:
            loaded_data = json.load(f)
            for group in loaded_data.values():
                for material, end_results in group.items():
                    # One material, possibly multiple end results
                    try:
                        try:
                            material_friendly = self.friendly_names[material]
                        except KeyError:
                            material_friendly =  material
                        for result, rarity_list in end_results.items():
                            rarity = rarity_list[0]
                            material_print = '{0} (Cent.) ({1})'.format(material_friendly, rarity)
                            self.recipes.add_edge(material_print, result)
                    except AttributeError:
                        # Some lists exist that need to be skipped.
                        pass

    def parse_recipes(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(FU_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(SB_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)

    def parse_drop_data(self):
        """Finds interesting drops from the loot tables."""
        # ToDo read treasure drop data treasure\cropharvest.treasurepools(.patch)
        pass

    def parse_extraction_data(self):
        with open(EXTRACTION_DATA, 'r') as f:
            loaded_data = json.load(f)
            for recipe in loaded_data:
                # There's always just one input, but can be multiple outputs
                input_unfriendly = next(iter(recipe['inputs'].keys()))
                try:
                    input_friendly = self.friendly_names[input_unfriendly]
                except KeyError:
                    input_friendly = input_unfriendly
                input_print = '{0} (Extr.)'.format(input_friendly)
                for output in recipe['outputs']:
                    self.recipes.add_edge(input_print, output)

    def parse_xeno_data(self):
        with open(XENO_DATA, 'r') as f:
            loaded_data = json.load(f)
            for recipe in loaded_data:
                # There's always just one input, but can be multiple outputs
                input_unfriendly = next(iter(recipe['inputs'].keys()))
                try:
                    input_friendly = self.friendly_names[input_unfriendly]
                except KeyError:
                    input_friendly = input_unfriendly
                input_print = '{0} (Xeno)'.format(input_friendly)
                for output in recipe['outputs']:
                    self.recipes.add_edge(input_print, output)

    def read_friendly_names(self):
        """Reads the more friendly names used within the game from the previously created file."""
        with open(FRIENDLY_NAMES, 'r') as f:
            for line in f:
                unfriendly_name, friendly_name = line.split(';')
                # stripping trailing whitespace
                friendly_name = friendly_name.strip()
                self.friendly_names[unfriendly_name] = friendly_name
                self.unfriendly_names[friendly_name] = unfriendly_name


class SbParserGUI(wx.Frame):
    def __init__(self, parent, title, parser):
        super().__init__(parent, title=title)
        self.parser = parser
        self._initialize()

    def _initialize(self):
        filtered_choices = []
        for name in nx.nodes(self.parser.recipes):
            try:
                filtered_choices.append(self.parser.friendly_names[name])
            except KeyError:
                filtered_choices.append(name)
        self.selector_wx = wx.ComboBox(self, choices=sorted(filtered_choices))
        self.tree_wx = wx.TreeCtrl(self)
        self.tree_wx.AddRoot(text='Select an item!')

        self.Bind(event=wx.EVT_COMBOBOX, handler=self._update_tree, source=self.selector_wx)

        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(self.selector_wx, pos=(0,0), flag=wx.EXPAND)
        sizer.Add(self.tree_wx, pos=(1,0), flag=wx.EXPAND)

        sizer.AddGrowableCol(idx=0)
        sizer.AddGrowableRow(idx=1)

        self.SetSizerAndFit(sizer)
        self.Center()
        self.Show()

    def _update_tree(self, event):
        """Updates TreeCtrl based on the combobox selection"""
        selected = self.selector_wx.GetStringSelection()
        self.tree_wx.DeleteAllItems()
        root = self.tree_wx.AddRoot(selected)

        # Going back to find all the prerequisites
        try:
            next_node = self.parser.unfriendly_names[selected]
        except KeyError:
            next_node = selected
        self._update_parent(parent=root, node=next_node)

    def _update_parent(self, parent, node):
        previous_nodes = self.parser.recipes.predecessors(node)
        for new_node in previous_nodes:
            try:
                new_text = self.parser.friendly_names[new_node]
            except KeyError:
                new_text = new_node
            new_parent = self.tree_wx.AppendItem(parent=parent, text=new_text)
            self._update_parent(parent=new_parent, node=new_node)


def dump_friendly_names(dump_file):
    """Reads the friendly names used within the game from the item and object folders and dumps them into a file."""
    skippables = ['.animation', '.bush', '.combofinisher', '.config', '.db', '.frames',
                  '.inspectiontool', '.lua', '.matmod', '.ogg', '.patch', '.png', '.projectile', '.recipe',
                  '.statuseffect', '.txt', '.unlock', '.wav', '.weaponability', '.weaponcolors']
    friendly_names = {}
    unfriendly_names = {}
    for item_file in chain(iglob('{0}/items/**/*.*'.format(SB_PATH), recursive=True),
                           iglob('{0}/items/**/*.*'.format(FU_PATH), recursive=True),
                           iglob('{0}/objects/**/*.*'.format(SB_PATH), recursive=True),
                           iglob('{0}/objects/**/*.*'.format(FU_PATH), recursive=True)):
        if any([to_skip in item_file for to_skip in skippables]):
            continue
        with open(item_file, 'r') as f:
            try:
                loaded_file = json.load(f)
                friendly_name = loaded_file['shortdescription']
                try:
                    unfriendly_name = loaded_file['itemName']
                except KeyError:
                    unfriendly_name = loaded_file['objectName']
                friendly_names[unfriendly_name] = filter_description(friendly_name)
                unfriendly_names[friendly_name] = unfriendly_name
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                with open(item_file, 'r') as f2:
                    read_file = f2.readlines()
                    friendly_line = next(line for line in read_file if 'shortdescription' in line)
                    friendly_name = friendly_line.split(':')[1].strip().strip('",')
                    try:
                        unfriendly_line = next(line for line in read_file if 'itemName' in line)
                    except StopIteration:
                        unfriendly_line = next(line for line in read_file if 'objectName' in line)
                    unfriendly_name = unfriendly_line.split(':')[1].strip().strip('",')
                    friendly_names[unfriendly_name] = filter_description(friendly_name)
                    unfriendly_names[friendly_name] = unfriendly_name
            except KeyError:
                print('KeyError at {0}'.format(item_file))

    with open(dump_file, 'w') as f:
        for key, value in friendly_names.items():
            f.write(f'{key};{value}\n')


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


def read_recipe(recipe_file):
    """Reads recipe json file and returns inputs and the output as tuple of generator exp and string"""
    with open(recipe_file, 'r') as f:
        loaded_file = json.load(f)
        output = loaded_file['output']['item']
        inputs = (x['item'] for x in loaded_file['input'])
    return inputs, output


def main():
    parser = SbParser()
    parser.read_friendly_names()
    parser.parse_recipes()
    parser.parse_centrifuge_data()
    parser.parse_extraction_data()
    parser.parse_xeno_data()
    #parser.parse_drop_data()
    #parser.parse_biome_data()
    app = wx.App()
    SbParserGUI(None, title="Rick's brain on Starbound", parser=parser)
    app.MainLoop()


if __name__ == '__main__':
    #dump_friendly_names(FRIENDLY_NAMES)
    main()
