import logging


class MetamodelCreationError(Exception):
    """
    Exception raised for errors in the textX metamodel creation process.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        logging.error(f"{self.__class__.__name__}: {self.message}")


class ModelCreationError(Exception):
    """
    Exception raised for errors in the textX model creation process.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        logging.error(f"{self.__class__.__name__}: {self.message}")
