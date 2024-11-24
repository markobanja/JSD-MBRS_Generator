import logging
import src.config as cfg


class PropertyType:
    """
    Class representing a property type.
    """
    def __init__(self, name, property_type, default_value, is_primary_key=False):
        """
        Constructor for the PropertyType class.
        """
        self.name = name
        self.type = property_type
        self.default_value = default_value
        self.is_primary_key = is_primary_key
        logging.debug(f'Creating PropertyType object with name: "{self.name}", type: "{self.type}", default_value: "{self.default_value}", is_primary_key: "{self.is_primary_key}"')

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
    def __init__(self, property_type, default_value=None, is_primary_key=True):
        super().__init__(self.__class__.__name__, property_type, default_value, is_primary_key)


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


class WrapperDataType(DataType):
    """
    Class representing a primitive wrapper data type, inheriting from data type.
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
        cfg.ID: IDType(cfg.ID, 'UUID.randomUUID()'),
        cfg.IDENTIFIER: IDType(cfg.IDENTIFIER, 'UUID.randomUUID()'),
        cfg.UNIQUE_ID: IDType(cfg.UNIQUE_ID, 'UUID.randomUUID()'),
        cfg.KEY: IDType(cfg.KEY, 'UUID.randomUUID()'),
        cfg.PRIMARY_KEY: IDType(cfg.PRIMARY_KEY, 'UUID.randomUUID()'),

        cfg.BYTE: PrimitiveDataType(cfg.BYTE, '0'),
        cfg.SHORT: PrimitiveDataType(cfg.SHORT, '0'),
        cfg.CHAR: PrimitiveDataType(cfg.CHAR, "'c'"),
        cfg.INT: PrimitiveDataType(cfg.INT, '0'),
        cfg.FLOAT: PrimitiveDataType(cfg.FLOAT, '0.0F'),
        cfg.LONG: PrimitiveDataType(cfg.LONG, '0L'),
        cfg.DOUBLE: PrimitiveDataType(cfg.DOUBLE, '0.0D'),
        cfg.BOOLEAN: PrimitiveDataType(cfg.BOOLEAN, 'false'),

        cfg.BYTE_W: WrapperDataType(cfg.BYTE_W, '0'),
        cfg.SHORT_W: WrapperDataType(cfg.SHORT_W, '0'),
        cfg.CHARACTER_W: WrapperDataType(cfg.CHARACTER_W, "'c'"),
        cfg.INTEGER_W: WrapperDataType(cfg.INTEGER_W, '0'),
        cfg.FLOAT_W: WrapperDataType(cfg.FLOAT_W, '0.0F'),
        cfg.LONG_W: WrapperDataType(cfg.LONG_W, '0L'),
        cfg.DOUBLE_W: WrapperDataType(cfg.DOUBLE_W, '0.0D'),
        cfg.BOOLEAN_W: WrapperDataType(cfg.BOOLEAN_W, 'false'),

        cfg.STR: OtherDataType(cfg.STR, '""'),
        cfg.STRING: OtherDataType(cfg.STRING, '""'),
        cfg.STRING_C: OtherDataType(cfg.STRING_C, '""'),

        cfg.DATE: DateType(cfg.DATE, 'LocalDate.of(1970, 01, 01)'),
        cfg.TIME: DateType(cfg.TIME, 'LocalTime.of(00, 00, 00, 00)'),
        cfg.DATETIME: DateType(cfg.DATETIME, 'LocalDateTime.of(1970, 01, 01, 00, 00, 00, 00)'),

        cfg.ARRAY: ListType(cfg.ARRAY, 'new ArrayList<{}>()'),
        cfg.LINKED: ListType(cfg.LINKED, 'new LinkedList<{}>()'),
        cfg.HASHMAP: ListType(cfg.HASHMAP, 'new HashMap<String, {}>()'),
        cfg.HASHSET: ListType(cfg.HASHSET, 'new HashSet<{}>()'),
        cfg.TREEMAP: ListType(cfg.TREEMAP, 'new TreeMap<String, {}>()'),
        cfg.LIST: ListType(cfg.LIST, '{}'),
    }
