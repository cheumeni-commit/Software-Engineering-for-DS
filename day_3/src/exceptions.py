# src/exceptions.py



class ACMEError(Exception):
    """Base exception class for all custom errors"""
    pass

class DatasetNotFoundError(ACMEError):
    """The dataset was not found on disk"""
    pass

class ModelUnknownError(ACMEError):
    """The requested model does not exist in the model registry"""
    pass
