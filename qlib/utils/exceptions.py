# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


# Base exception class
class QlibException(ValueError):
    pass


class RecorderInitializationError(Exception):
    """Error type for re-initialization when starting an experiment"""


class LoadObjectError(RuntimeError):
    """Error type for Recorder when can not load object"""


class ExpAlreadyExistError(QlibException):
    """Experiment already exists"""
