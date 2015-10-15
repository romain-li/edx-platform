from pkg_resources import resource_exists, resource_listdir, resource_isdir, resource_filename
import os
import sys

from xblock.core import XBlock

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.storage import FileSystemStorage
from django.core.files.storage import Storage


class PackageStorage(Storage):
    """
    Storage implementation for Python packages.

    TODO: does this really not already exist?
    """
    RESOURCE_PREFIX = 'xblock/resources/'

    def __init__(self, module, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        super(PackageStorage, self).__init__(*args, **kwargs)
        self.module = module

        # Register a prefix that collectstatic will add to each path
        self.prefix = os.path.join(self.RESOURCE_PREFIX, module)

    def path(self, name):
        """
        Returns a file system filename for the specified file name.
        """
        return resource_filename(self.module, name)

    def exists(self, path):
        """
        Returns True if the specified path exists.
        """
        return resource_exists(self.module, path)

    def listdir(self, path):
        """
        Lists the directories beneath the specified path.
        """
        directories = []
        files = []
        for item in resource_listdir(self.module, path):
            __, file_extension = os.path.splitext(item)
            if not file_extension in [".py", ".pyc", ".scss"]:
                if resource_isdir(self.module, os.path.join(path, item)):
                    directories.append(item)
                else:
                    files.append(item)
        return directories, files

    def open(self, name, mode='rb'):
        """
        Retrieves the specified file from storage.
        """
        path = self.path(name)
        return FileSystemStorage(path).open(path, mode)


class XBlockPipelineFinder(BaseFinder):
    """
    A static files finder that gets static assets from xblocks.
    """
    storage_class = FileSystemStorage

    def __init__(self, *args, **kwargs):
        super(XBlockPipelineFinder, self).__init__(*args, **kwargs)
        installed_xblock_packages = set()
        for __, xblock_class in XBlock.load_classes():
            if self._is_installed_xblock(xblock_class):
                installed_xblock_packages.add(xblock_class.__module__)
        self.package_storages = list(PackageStorage(package) for package in installed_xblock_packages)

    def _is_installed_xblock(self, xblock_class):
        """
        Returns true if the specified XBlock class belongs to an installed package,
        i.e. it is not defined in edx-platform.
        """
        file = sys.modules[xblock_class.__module__].__file__
        return not "edx-platform" in file

    def list(self, ignore_patterns):
        """
        List all static files in all xblock packages.
        """
        for storage in self.package_storages:
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    yield path, storage

    def find(self, path, all=False):
        """
        Looks for files in the xblock package directories.
        """
        matches = []
        for storage in self.package_storages:
            if storage.exists(path):
                match = storage.path(path)
                if not all:
                    return match
                matches.append(match)
        return matches
