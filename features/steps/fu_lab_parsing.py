#!/usr/bin/env python
# -*- coding: utf-8 -*-

from behave import *


@when("centrifuge recipes are parsed")
def parsing_centrifuge_recipes(context):
    raise NotImplementedError


@when("extraction recipes are parsed")
def parsing_extraction_recipes(context):
    raise NotImplementedError


@when("xeno recipes are parsed")
def parsing_xeno_recipes(context):
    raise NotImplementedError


@then(
    "centrifuge extracting magmacomb produces corefragmentore at normal and liquidlava at common and scorchedcore at rare")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("lab extracting choppedonion produces tissueculture")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("xeno extracting ignuschiliseed nakatibark produces gene_reactive and gene_pyro")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass
