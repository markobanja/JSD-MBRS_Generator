import logging


class PropertyType:
    """
    Class representing a property type.
    """
    def __init__(self, name, property_type, default_value):
        """
        Constructor for the PropertyType class.
        """
        self.name = name
        self.type = property_type
        self.default_value = default_value
        logging.debug(f'Created "{self.name}" class with type "{self.type}" and default value "{self.default_value}"')

    def __str__(self):
        """
        Returns the string representation of the PropertyType class.
        """
        return f"{self.name}(type={self.type}, default_value={self.default_value})"
    
    def set_default_value(self, default_value):
        """
        Method to set the default PropertyType value.
        """
        self.default_value = default_value
        logging.debug(f"Setting default value of '{self.name}' class to '{self.default_value}'")
 
    def get_default_value(self):
        """
        Method to get the default PropertyType value.
        """
        logging.debug(f"Getting default value of '{self.name}' class")
        return self.default_value


class IDType(PropertyType):
    """
    Class representing an ID type.
    """
    def __init__(self, property_type, default_value=None):
        super().__init__(self.__class__.__name__, property_type, default_value)


class DataType(PropertyType):
    """
    Abstract class representing a data type.
    """
    def __init__(self, name, property_type, default_value=None):
        super().__init__(name, property_type, default_value)


class PrimitiveDataType(DataType):
    """
    Class representing a primitive data type, inheriting from data type.
    """
    def __init__(self, property_type, default_value=None):
        super().__init__(self.__class__.__name__, property_type, default_value)


class OtherDataType(DataType):
    """
    Class representing other data type, inheriting from data type.
    """
    def __init__(self, property_type, default_value=None):
        super().__init__(self.__class__.__name__, property_type, default_value)


class DateType(PropertyType):
    """
    Class representing a date type.
    """
    def __init__(self, property_type, default_value=None):
        super().__init__(self.__class__.__name__, property_type, default_value)


class ListType(PropertyType):
    """
    Class representing a list type.
    """
    def __init__(self, property_type, default_value=None):
        super().__init__(self.__class__.__name__, property_type, default_value)


def get_type_builtins():
    """
    Returns a dictionary of built-in types.
    """
    logging.info('Creating type builtins')
    return {
        'id': IDType('id', 0),
        'identifier': IDType('identifier', 0),
        'uniqueId': IDType('uniqueId', 0),
        'key': IDType('key', 0),
        'primaryKey': IDType('primaryKey', 0),

        'byte': PrimitiveDataType('byte'),
        'short': PrimitiveDataType('short'),
        'char': PrimitiveDataType('char'),
        'int': PrimitiveDataType('int'),
        'integer': PrimitiveDataType('integer'),
        'float': PrimitiveDataType('float'),
        'long': PrimitiveDataType('long'),
        'double': PrimitiveDataType('double'),
        'boolean': PrimitiveDataType('boolean'),

        'string': OtherDataType('string'),
        'constant': OtherDataType('constant'),

        'date': DateType('date', '1970-01-01'),
        'time': DateType('time', '00:00:00'),
        'datetime': DateType('datetime', '1970-01-01T00:00:00+00:00'),

        'array': ListType('array'),
        'linked': ListType('linked'),
        'list': ListType('list'),
        'set': ListType('set'),
    }