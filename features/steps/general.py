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
