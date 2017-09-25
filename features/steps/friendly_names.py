from behave import *


@when("friendly names are read")
def friendly_names_read(context):
    context.parser.read_friendly_names()


@then("unfriendly name {unfriendly} corresponds to friendly name {friendly}")
def assume_unfriendly_friendly(context, unfriendly, friendly):
    try:
        assert(context.parser.friendly_names[unfriendly] == friendly)
    except:
        print(context.parser.friendly_names)
        raise


@then("friendly name {friendly} corresponds to unfriendly name {unfriendly}")
def assume_friendly_unfriendly(context, friendly, unfriendly):
    try:
        assert(context.parser.unfriendly_names[friendly] == unfriendly)
    except:
        print(context.parser.unfriendly_names)
        raise
