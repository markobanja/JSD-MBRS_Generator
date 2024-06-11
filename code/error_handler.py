import logging

class MetamodelCreationError(Exception):
    """
    Exception raised for errors in the textx metamodel creation process.
    """
    def __init__(self, message="Failed to create the textx grammar metamodel."):
        self.message = message
        super().__init__(self.message)
        logging.error(f"{self.__class__.__name__}: {self.message}")

class ModelCreationError(Exception):
    """
    Exception raised for errors in the textx model creation process.
    """
    def __init__(self, message="Failed to create the textx grammar model."):
        self.message = message
        super().__init__(self.message)
        logging.error(f"{self.__class__.__name__}: {self.message}")