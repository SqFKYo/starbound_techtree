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
from itertools import chain
import json
import networkx as nx
import os
import re
import wx

BIOME_FOLDER_FU = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse\biomes'
BIOME_FOLDER_SB = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets\biomes'
CENTRIFUGE_DATA = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse\objects\generic\centrifuge_recipes.config'
# Note: Comments have been removed from the drop data files to facilitate json loading
DROP_DATA_FU = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse\treasure\cropharvest.treasurepools.patch'
DROP_DATA_SB = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets\treasure\cropharvest.treasurepools'
EXTRACTION_DATA = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse\objects\generic\extractionlab_recipes.config'
FRIENDLY_NAMES = 'friendly_names.csv'
FU_PATH = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse'
RECIPES = 'recipes.yaml'
SB_PATH = r'C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets'
XENO_DATA = r'C:\Games\Steam\steamapps\common\Starbound\FrackinUniverse\objects\generic\xenostation_recipes.config'


class SbParser(object):
    def __init__(self):
        self.friendly_names = {}
        self.recipes = nx.DiGraph()
        self.skippable_recipes = set()
        self.unfriendly_names = {}

    def determine_skippable_recipes(self):
        """If recipes are overwritten in FU, do not read them from standard SB"""
        # ToDo skippable recipes
        sb_recipes = set(os.path.basename(path)
                         for path
                         in iglob('{0}/recipes/**/*.recipe'.format(SB_PATH), recursive=True))
        fu_recipes = set(os.path.basename(path)
                         for path
                         in iglob('{0}/recipes/**/*.recipe'.format(FU_PATH), recursive=True))
        self.skippable_recipes = sb_recipes.intersection(fu_recipes)

    def parse_atmosphere_data(self):
        # ToDo parse Atmospheric Condenser recipes
        print('atmosphere data not read!')

    def parse_biome_data(self):
        """Parses the mainBlock and subBlocks data found in the biome files."""
        for biome_file in chain(iglob('{0}/biomes/**/*.*'.format(SB_PATH), recursive=True),
                                iglob('{0}/biomes/**/*.*'.format(FU_PATH), recursive=True)):
            with open(biome_file, 'r') as f:
                read_file = f.readlines()
                try:
                    name_line = read_file[1]
                    main_line = next(line for line in read_file if 'mainBlock' in line)
                    sub_line = next(line for line in read_file if 'subBlocks' in line)
                    if '"op"' in main_line or '"op"' in sub_line:
                        # Skipping patch operations lines when matching
                        continue
                    filtered_name = name_line.split(':')[1].strip().strip('",')
                    try:
                        friendly_name = self.friendly_names[filtered_name]
                    except KeyError:
                        friendly_name = filtered_name
                    # Main block
                    filtered_main = main_line.split(':')[1].strip().strip('",')
                    self.recipes.add_edge(f'{friendly_name} (biome)', filtered_main)
                    # Sub blocks
                    sub_match = re.search(r'".+"', sub_line.split(':')[1])
                    sub_match_processed = sub_match.group().replace('"', '')
                    sub_list = [sub.strip() for sub in sub_match_processed.split(',')]
                    for sub in sub_list:
                        self.recipes.add_edge(f'{friendly_name} (biome)', sub.strip('"'))
                except StopIteration:
                    # No block definitions found in biome file
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
                            material_friendly = material
                        for result, rarity_list in end_results.items():
                            rarity = rarity_list[0]
                            material_print = '{0} (Cent.) ({1})'.format(material_friendly, rarity)
                            self.recipes.add_edge(material_print, result)
                    except AttributeError:
                        # Some lists exist that need to be skipped.
                        pass

    def parse_harvest_data(self):
        """
        Finds interesting drops from the farming loot tables. Interesting loot is defined as something else
        than the plant itself, its seed or plantfibre.
        """
        with open(DROP_DATA_SB, 'r') as f:
            data = json.load(f)
            for harvest, results in data.items():
                skippables = ['plantfibre']
                harvest_name = harvest.split('Harvest')[0]
                skippables.append(harvest_name)
                skippables.append(f'{harvest_name}seed')
                result_pool = results[0][1]['pool']
                for pool in result_pool:
                    if pool['item'] not in skippables:
                        try:
                            friendly_harvest = self.friendly_names[harvest_name]
                        except KeyError:
                            friendly_harvest = harvest_name
                        self.recipes.add_edge(f'{friendly_harvest} (Harv.)', pool['item'])
        with open(DROP_DATA_FU, 'r') as f:
            data = json.load(f)
            for group in data:
                skippables = ['plantfibre']
                harvest_name = group['path'].split('Harvest')[0].strip('/')
                skippables.append(harvest_name)
                skippables.append(f'{harvest_name}seed')
                result_pool = group['value'][0][1]['pool']
                for pool in result_pool:
                    if pool['item'] not in skippables:
                        try:
                            friendly_harvest = self.friendly_names[harvest_name]
                        except KeyError:
                            friendly_harvest = harvest_name
                        try:
                            self.recipes.add_edge(f'{friendly_harvest} (Harv.)', pool['item'])
                        except TypeError:
                            self.recipes.add_edge(f'{friendly_harvest} (Harv.)', pool['item'][0])

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

    def parse_liquid_data(self):
        # ToDo parse Liquid Collector recipes
        print('liquid data not read!')

    def parse_materials(self):
        """
        Reads the .material files to change the found materialName nodes in the recipes into found itemDrop names.

        This is done to facilitate easier searching for extractable blocks.
        """
        for material_file in chain(iglob('{0}/tiles/materials/**/*.material'.format(SB_PATH), recursive=True),
                                   iglob('{0}/tiles/materials/**/*.material'.format(FU_PATH), recursive=True)):
            with open(material_file, 'r') as f:
                try:
                    loaded_file = json.load(f)
                    old_label = loaded_file['materialName']
                    new_label = loaded_file['itemDrop']
                    if old_label != new_label:
                        self.recipes = nx.relabel_nodes(self.recipes, mapping={old_label: new_label})
                except json.decoder.JSONDecodeError:
                    print(f'JSONDecodeError at {material_file}!')
                except KeyError:
                    print(f'KeyError at {material_file}!')

    def parse_recipes(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(FU_PATH), recursive=True):
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)
        for recipe_file in iglob('{0}/recipes/**/*.recipe'.format(SB_PATH), recursive=True):
            if os.path.basename(recipe_file) in self.skippable_recipes:
                # Skipping recipe overwritten by FU
                continue
            materials, result = read_recipe(recipe_file)
            for material in materials:
                self.recipes.add_edge(material, result)

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

    def read_and_dump_recipes(self, recipe_file=RECIPES):
        """Reads recipes and then pickles the graph to a file"""
        self.parse_biome_data()
        self.parse_materials()

        self.determine_skippable_recipes()
        self.parse_recipes()
        self.parse_centrifuge_data()
        self.parse_extraction_data()
        self.parse_xeno_data()
        self.parse_harvest_data()

        self.parse_liquid_data()
        self.parse_atmosphere_data()
        nx.write_yaml(self.recipes, recipe_file)

    def read_friendly_names(self):
        """Reads the more friendly names used within the game from the previously created file."""
        with open(FRIENDLY_NAMES, 'r') as f:
            for line in f:
                unfriendly_name, friendly_name = line.split(';')
                # stripping trailing whitespace
                friendly_name = friendly_name.strip()
                self.friendly_names[unfriendly_name] = friendly_name
                self.unfriendly_names[friendly_name] = unfriendly_name

    def read_recipes(self, recipe_file=RECIPES):
        """Reads recipe from previously saved pickle file."""
        self.recipes = nx.read_yaml(recipe_file)


class SbParserGUI(wx.Frame):
    def __init__(self, parent, title, parser):
        super().__init__(parent, title=title)
        self.parser = parser
        self._initialize()

    def _initialize(self):
        filtered_choices = []
        for name in nx.nodes(self.parser.recipes):
            # Only take recipe results, not the materials
            if not self.parser.recipes.predecessors(name):
                continue
            try:
                filtered_choices.append(self.parser.friendly_names[name])
            except KeyError:
                filtered_choices.append(name)
        self.selector_wx = wx.ComboBox(self, choices=sorted(filtered_choices))
        self.tree_wx = wx.TreeCtrl(self)
        self.tree_wx.AddRoot(text='Select an item!')

        self.Bind(event=wx.EVT_COMBOBOX, handler=self._update_tree, source=self.selector_wx)

        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(self.selector_wx, pos=(0, 0), flag=wx.EXPAND)
        sizer.Add(self.tree_wx, pos=(1, 0), flag=wx.EXPAND)

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
        try:
            previous_nodes = self.parser.recipes.predecessors(node)
            for new_node in previous_nodes:
                try:
                    new_text = self.parser.friendly_names[new_node]
                except KeyError:
                    new_text = new_node
                new_parent = self.tree_wx.AppendItem(parent=parent, text=new_text)
                self._update_parent(parent=new_parent, node=new_node)
        except nx.exception.NetworkXError:
            # Item that can't be obtained by crafting encountered
            pass


def dump_friendly_names(dump_file):
    """Reads the friendly names used within the game from the item and object folders and dumps them into a file."""
    skippables = ['.animation', '.bush', '.combofinisher', '.config', '.db', '.frames',
                  '.inspectiontool', '.lua', '.matmod', '.ogg', '.patch', '.png', '.projectile', '.recipe',
                  '.statuseffect', '.txt', '.unlock', '.wav', '.weaponability', '.weaponcolors']
    friendly_names = {}
    for item_file in chain(iglob('{0}/items/**/*.*'.format(SB_PATH), recursive=True),
                           iglob('{0}/items/**/*.*'.format(FU_PATH), recursive=True),
                           iglob('{0}/objects/**/*.*'.format(SB_PATH), recursive=True),
                           iglob('{0}/objects/**/*.*'.format(FU_PATH), recursive=True),
                           iglob('{0}/biomes/**/*.*'.format(SB_PATH), recursive=True),
                           iglob('{0}/biomes/**/*.*'.format(FU_PATH), recursive=True)):
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
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                with open(item_file, 'r') as f2:
                    read_file = f2.readlines()
                    try:
                        friendly_line = next(line for line in read_file if 'shortdescription' in line)
                    except StopIteration:
                        # .biome file
                        friendly_line = next(line for line in read_file if 'friendlyName' in line)
                    friendly_name = friendly_line.split(':')[1].strip().strip('",')
                    try:
                        # .item files
                        unfriendly_line = next(line for line in read_file if 'itemName' in line)
                    except StopIteration:
                        try:
                            # .object files
                            unfriendly_line = next(line for line in read_file if 'objectName' in line)
                        except StopIteration:
                            # .biome files
                            unfriendly_line = next(line for line in read_file if 'name' in line)
                    unfriendly_name = unfriendly_line.split(':')[1].strip().strip('",')
                    friendly_names[unfriendly_name] = filter_description(friendly_name)
            except KeyError:
                print(f'KeyError at {item_file}')
            except StopIteration:
                print(f'StopIteration at {item_file}')

    # If multiple unfriendly names point to the same friendly name, we need to distinguish them!
    unfriendly_names = defaultdict(list)
    for unfriendly, friendly in friendly_names.items():
        unfriendly_names[friendly].append(unfriendly)

    friendly_names = {}
    for friendly, unfriendlies in unfriendly_names.items():
        if len(unfriendlies) > 1:
            for i, unfriendly in enumerate(unfriendlies, start=1):
                friendly_names[unfriendly] = f'{friendly} ({i})'
        else:
            friendly_names[unfriendlies[0]] = friendly

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
        try:
            loaded_file = json.load(f)
            output = loaded_file['output']['item']
            inputs = (x['item'] for x in loaded_file['input'])
        except json.decoder.JSONDecodeError:
            print(f"Couldn't read {recipe_file}")
            inputs, output = ([None], 'None')
    return inputs, output


def main():
    parser = SbParser()
    parser.read_friendly_names()

    # parser.read_and_dump_recipes()
    parser.read_recipes()

    app = wx.App()
    SbParserGUI(None, title="Rick's brain on Starbound", parser=parser)
    app.MainLoop()


if __name__ == '__main__':
    # dump_friendly_names(FRIENDLY_NAMES)

    # Changing the cwd to the script folder
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main()
