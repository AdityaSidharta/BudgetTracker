from emoji import emojize


def append_emoji(x, input_dict):
    if x in input_dict:
        return emojize(x + "   " + input_dict[x]["emoji"], use_aliases=True)
    else:
        return x + "   "
