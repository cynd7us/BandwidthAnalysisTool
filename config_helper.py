import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")


def read_config_map(section):
    """
    this function handles parsing the config file
    and reading specific value from a specific section.
    :param section: specified section from the config file
    :return: void
    """
    data = {}
    options = config.options(section)
    for option in options:
        try:
            data[option] = config.get(section, option)
            if data[option] is -1:
                print "skip: %s" % option
        except IndexError:
            print "Exception on %s " % option
            data[option] = None
    return data


def update_key_value(section, key, value):
    """
    update specified key to a certain value
    from the configuration file
    :param section: specified section
    :param key: key to update
    :param value: new value
    :return: void
    """
    config.set(section, key, value)
    with open("config.ini", "wb") as configfile:
        config.write(configfile)
