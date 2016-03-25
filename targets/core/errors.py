# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class TargetsException(Exception):
    """
        Base class for generic package related exceptions.
        """
    pass


class FileSystemException(TargetsException):
    """
    Base class for generic file system exceptions.
    """
    pass


class FileAlreadyExists(FileSystemException):
    """
    Raised when a file system operation can't be performed because
    a directory exists but is required to not exist.
    """
    pass


class MissingParentDirectory(FileSystemException):
    """
    Raised when a parent directory doesn't exist.
    (Imagine mkdir without -p)
    """
    pass


class NotADirectory(FileSystemException):
    """
    Raised when a file system operation can't be performed because
    an expected directory is actually a file.
    """
    pass


class InvalidDeleteException(FileSystemException):
    pass


class FileNotFoundException(FileSystemException):
    pass
