
def config2kwargs(config):
    """Takes a ConfigParser object and converts it to the dotted kwargs
    format excpected by Jala
    """
    kwargs = {}
    for section in config:
        for option, value in config.items(section):
            kwargs['%s.%s' % (section, option)] = value
    return kwargs
