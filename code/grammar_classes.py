import logging


class IDType:
    """
    Class representing an ID type.
    """
    def __init__(self, type):
        """
        Constructor for the IDType class.
        """
        self.type = type
        logging.debug(f'Created IDType with type {self.type}')

    def __str__(self):
        """
        Returns the string representation of the IDType.
        """
        return self.type

class DataType:
    """
    Class representing a data type.
    """
    def __init__(self, type):
        """
        Constructor for the DataType class.
        """
        self.type = type
        logging.debug(f'Created DataType with type {self.type}')

    def __str__(self):
        """
        Returns the string representation of the DataType.
        """
        return self.type

def get_type_builtins():
    """
    Returns a dictionary of built-in types.
    """
    logging.info('Creating type builtins')
    return {
        'id': IDType('id'),
        'identificator': IDType('identificator'),

        'boolean': DataType('boolean'),
        'byte': DataType('byte'),
        'short': DataType('short'),
        'char': DataType('char'),
        'integer': DataType('integer'),
        'long': DataType('long'),
        'float': DataType('float'),
        'double': DataType('double'),

        'string': DataType('string'),
        'constant': DataType('constant'),
    }