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
from matplotlib import pyplot as plt
import networkx as nx

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
        
    def draw_high_tech_trees(self, height):
        """Draw tech trees that are at least 'height' high and on top"""
        # ToDo
        # Find out the topmost nodes, which are end points of the graph
        top_nodes = [x for x in self.recipes.nodes_iter() if self.recipes.out_degree(x)==0]
        
        # How far is the longest distance from the bottom to the top of the highest peak
        high_nodes = [x for x in self.recipes.nodes_iter() if max(self.get_dijkstra_distance(target=x))>=height]
        for node in high_nodes:
            plt.clf()
            self.draw_tech_tree(node)
        
        
    def draw_highly_usable_techs(self, nodes_out):
        """
        Draw tech trees for the materials that are used in multiple other recipes.
        
        This material needs to have at least one node in, so that it's not trivial.
        """
        high_use = [x for x in self.recipes.nodes_iter() if (self.recipes.out_degree(x)>=nodes_out and self.recipes.in_degree(x)>1)]
        for node in high_use:
            plt.clf()
            self.draw_tech_tree(node)
        
    def draw_tech_tree(self, node):
        """Draws tech tree leading to the selected node."""
        self.labels = {}
        self.next_xs = defaultdict(int)
        self.positions = {}
        self.interesting_nodes = [node]
        self.interesting_edges = []
        highest_point = max(self.get_dijkstra_distance(target=node))
        self.positions[node] = (0,highest_point)
        
        preds = self.recipes.pred[node]
        try:
            self.labels[node] = self.friendly_names[node]
        except KeyError:
            # DEBUG
            print('missing description: {0}'.format(node))
            self.labels[node] = node
        self.interesting_nodes.extend(preds)
        self.interesting_edges.extend(self.recipes.in_edges(nbunch=[node]))
        for pred in preds:
            self.get_children(pred, highest_point-1)
            
        # Constructing other graph for drawing purposes
        h = nx.DiGraph()
        h.add_nodes_from(self.interesting_nodes)
        h.add_edges_from(self.interesting_edges)
        
        widest_point = max(x for x in self.next_xs.values())
        
        nx.draw(h, pos=self.positions, labels=self.labels, with_labels=True)
        
        height = highest_point*Y_MODIFIER
        width = widest_point*X_MODIFIER
        figure = plt.gcf()
        figure.set_size_inches(width,height)
        plt.savefig("{0}.png".format(self.labels[node]), dpi=200)
        #plt.show()
        
    def get_children(self, node, height):
        """
        Gets the children of the node, and adds the positions, nodes and edges related
        to the according lists.
        """
        try:
            self.positions[node]
        except KeyError:
            self.positions[node] = (self.next_xs[height],height)
            self.next_xs[height] += X_OFFSET
            preds = self.recipes.pred[node]
            self.interesting_nodes.extend(preds)
            self.interesting_edges.extend(self.recipes.in_edges(nbunch=[node]))
            try:
                self.labels[node] = self.friendly_names[node]
            except KeyError:
                self.labels[node] = node
            for pred in preds:
                self.get_children(pred, height-1)
        
    def get_children_positions(self, children, height):
        if not children or height < 0:
            return
        for child in children:
            try:
                self.positions[child]
            except KeyError:
                self.positions[child] = (self.next_xs[height],height)
                self.next_xs[height] += X_OFFSET
            self.get_children_positions(self.recipes.pred[child], height-1)
        
    def get_dijkstra_distance(self, target):
        for node in self.recipes.nodes_iter():
            try:
                yield nx.dijkstra_path_length(self.recipes, source=node, target=target)
            except nx.NetworkXNoPath:
                yield 0
        
    def get_tech_positions(self):
        # What is the next value for x if y is given? Access the dict with the y value and then increment the value by 1!
        self.next_xs = defaultdict(int)
        self.positions = {}
        
        # Find out the topmost nodes, which are end points of the graph
        top_nodes = [x for x in self.recipes.nodes_iter() if self.recipes.out_degree(x)==0]
        
        # How far is the longest distance from the bottom to the top of the highest peak
        highest_point = max(max(self.get_dijkstra_distance(target=top)) for top in top_nodes)
        
        # Try to access position, if not available, then make a new one!
        for node in top_nodes:
            try:
                self.positions[node]
            except KeyError:
                self.positions[node] = (self.next_xs[highest_point],highest_point)
                self.next_xs[highest_point] += 1
            self.get_children_positions(self.recipes.pred[node], highest_point-1)
        
    def parse_craftables(self):
        """Parses all the recipes into NetworkX DiGraph object."""
        for recipe_file in iglob('**/*.recipe', recursive=True):
        #for recipe_file in iglob('./ff_stations/prototyper/*.recipe', recursive=True):
            self.parse_recipe_file(recipe_file)
        
    def parse_drop_data(self):
        """Finds interesting drops from the loot tables."""
        # ToDo
        pass

    def parse_extraction_data(self):
        with open(EXTRACTION_DATA, 'r') as extract:
            for line in extract:
                self.parse_lua_recipe(line, source='extract')
            
    def parse_lua_recipe(self, line, source):
        """
        Takes in recipe_line of text such as:
        {inputs = { liquidwater=10 }, outputs = { fu_salt=1, fu_oxygen=1, fu_hydrogen=1 }, time = 0.75},
        and returns recipe-object, which has inputs and outputs as attribute dictionaries.
        """
        if '{inputs' in line:
            split_text = line.split('{')
            inputs = split_text[2]
            outputs = split_text[3]
            inputs = inputs.split('}')[0].strip()
            outputs = outputs.split('}')[0].strip()
            inputs = tuple(i.strip() for i in inputs.split('='))
            if source == 'xeno':
                self.xeno_recipes[inputs] = outputs
                for output in outputs.split(','):
                    self.xeno_sources[output.split('=')[0].strip()].append(inputs)
            elif source == 'extract':
                self.extractor_recipes[inputs] = outputs
                for output in outputs.split(','):
                    self.extractor_sources[output.split('=')[0].strip()].append(inputs)
 
    def parse_recipe_file(self, input_file):
        """Recipe files define first inputs and then outputs."""
        raws = []
        result = None
        reading_input = False
        reading_output = False
        
        with open(input_file, 'r') as recipe_file:
            for line in recipe_file:
                if reading_input:
                    if ']' in line:
                        reading_input = False
                        continue
                    try:
                        raws.append(line.split(':')[1].split(',')[0].split('"')[1])
                    except IndexError:
                        pass
                    
                elif reading_output:
                    result = line.split(':')[1].split('"')[1]
                    # Output is always just one line
                    reading_output = False
                elif '"input"' in line:
                    reading_input = True
                elif '"output"' in line:
                    if '"item"' in line:
                        # Item defined on the same line
                        result = line.split(':')[2].split(',')[0].split('"')[1]
                    else:
                        # Item defined on another line
                        reading_output = True
                # Recipe parsed, adding to graph
                if not reading_output and not reading_input and raws and result:
                    # Checking if result and/or raws are already in the graph, adding if necessary
                    if result not in self.recipes:
                        self.recipes.add_node(result)
                    for raw in raws:
                        if raw not in self.recipes:
                            self.recipes.add_node(raw)
                        # Same for edges
                        if not self.recipes.has_edge(raw, result):
                            self.recipes.add_edge(raw, result)
                    break
    
    def parse_xeno_data(self):
        with open(XENO_DATA, 'r') as xeno:
            for line in xeno:
                self.parse_lua_recipe(line, source='xeno')
                    
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
            
    def show_tech_tree(self):
        """Prints the tech tree (crafting recipes) on screen as a figure."""
        self.get_tech_positions()
        # Drawing *all* recipes
        nx.draw(self.recipes, pos=self.positions, with_labels=True)
        plt.show()
        
def dump_ext_xeno_to_files(parser):
    """Dumps the xeno and extractor data to text files."""
    parser.parse_extraction_data()
    parser.parse_xeno_data()
    with open('xeno_sources.txt', 'w') as xenos:
        for key, value in sorted(parser.xeno_sources.items()):
            xenos.write("{0}: {1}\n".format(key, value))
    with open('ext_sources.txt', 'w') as ext:
        for key, value in sorted(parser.extractor_sources.items()):
            ext.write("{0}: {1}\n".format(key, value))
       
def dump_names_to_file(parser):
    """Dumps the (un)friendly names to text file."""
    with open('sb_names.txt', 'w') as names:
        for key, value in sorted(parser.unfriendly_names.items()):
            names.write("{0}: {1}\n".format(key, value))
        
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
    # ToDo reading from file
    #parser.read_friendly_names(from_file='sb_names.txt')
    #parser.read_ext(from_file='ext_sources.txt')
    #parser.read_xeno(from_file='xeno_sourcex.txt')
    
    parser.read_friendly_names()
    
    parser.parse_craftables()
    # ToDo add extracts and xeno lab results to recipes
    #parser.add_ext_xeno_crafts()
    
    #parser.show_tech_tree()
    #parser.draw_tech_tree(parser.unfriendly_names['Nuclear Core'])
    #parser.draw_tech_tree(parser.unfriendly_names['Advanced Plastic'])
    #parser.draw_tech_tree('designlab')
    parser.draw_tech_tree('protocitebar')
    #parser.draw_highly_usable_techs(nodes_out=3)
    #parser.draw_high_tech_trees(height=5)

if __name__ == '__main__':
    main()

