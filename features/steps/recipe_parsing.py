#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *
import networkx as nx
from nose.tools import assert_in


@when("crafting recipes are parsed")
def parsing_crafting_recipes(context):
    context.parser.parse_crafting_recipes()


@then("{recipe_name} recipe is found")
def assume_recipe_found(context, recipe_name):
    assert_in(recipe_name, nx.nodes(context.parser.crafting_recipes))


@then("{result} is crafted using {materials}")
def assume_recipe_input_output(context, result, materials):
    raws = materials.split(' and ')
    for raw in raws:
        assert_in((raw, result), nx.edges(context.parser.crafting_recipes))
