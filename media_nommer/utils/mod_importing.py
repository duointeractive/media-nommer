"""
Some utilities for importing modules.
"""
def import_class_from_module_string(fqpn_str):
    """
    Given a FQPN for a class, import and return the class.
    
    :param str fqpn_str: The FQPN to the class to import.
    :returns: The class given in the FQPN.
    """
    components = fqpn_str.split('.')
    # Generate a FQPN with everything but the class name.
    nom_module_str = '.'.join(components[:-1])
    # Just the target module to import.
    class_name = components[-1]
    # Import the class's module and the class itself.
    nommer = __import__(nom_module_str, globals(), locals(), [class_name])

    try:
        return getattr(nommer, class_name)
    except AttributeError:
        raise ImportError('No class named %s' % class_name)
