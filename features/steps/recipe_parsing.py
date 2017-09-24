#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *
import sb_parser as sb


@given("vanilla Starbound folder is {folder}")
def set_vanilla_folder(context, folder):
    context.vanilla_folder = folder


@given("Frackin' Universe folder is {folder}")
def set_fu_folder(context, folder):
    context.fu_folder = folder


@when("SbParser is initialized")
def initializing_sb_parser(context):
    context.parser = sb.SbParser()


@when("crafting recipes are parsed")
def parsing_crafting_recipes(context):
    raise NotImplementedError


@then("{recipe_name} recipe is found")
def assume_recipe_found(context, recipe_name):
    raise NotImplementedError


@then("{result} is crafted using {materials}")
def assume_recipe_input_output(context, result, materials):
    """materials is a list seperated by ' and '"""
    raise NotImplementedError
