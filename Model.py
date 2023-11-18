# Copyright (c) 2023 The Old Man and the C
#
# This file is part of mvcTkinter.
#
# mvcTkinter is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# mvcTkinter is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with mvcTkinter. If not, see <https://www.gnu.org/licenses/>.

# Model superclass
# Provides connections to a controller object
# Options:
# controller, name
# TODO: formalize model interaction with controller?

from .core.OptionsMixin import OptionsMixin


class Model(OptionsMixin):
    def __init__(self, **options):
        self.options = options
        self._name = self.option("name")
        self._controller = None
        self.setController(self.option("controller"))

    # This method returns the name of the controller. Provided only to keep
    # in line with the rest of the MVC spec.
    def name(self):
        return self._name

    # This method returns the controller object for this model.
    def controller(self):
        return self._controller

    # This method sets the controller object for this model. If the model
    # is already registered with a controller, it will be unregistered from
    # that controller and registered to the new one.
    def setController(self, controller):
        if self.controller() == controller:
            return
        if self.controller() is not None:
            self.controller().setModel(None)
        self._controller = controller
        self.controller().setModel(self)

    # Convenience method definitions for controller access to cut down on code
    # volume:

    def _settingValue(self, setting):
        return self.controller().settingValue(setting)

    def _setSetting(self, setting, value, write=True):
        self.controller().setSetting(setting, value, write)

    def _output(self, key=None, *args):
        self.controller().output(key, *args)

    def _dataForModel(self, key, **kwargs):
        return self.controller().dataForModel(key, **kwargs)

    def _modelUpdated(self, key, **kwargs):
        return self.controller().modelUpdated(key, **kwargs)

    def _currentDir(self):
        return self._dataForModel("currentDir")

    def _pathExists(self, path):
        return self._dataForModel("pathExists", path=path)

    def _latestFile(self, directory, extension=""):
        return self._dataForModel("latestFile", directory=directory,
                                  extension=extension)

    def _readFile(self, file, **kwargs):
        return self._dataForModel("readFile", file=file, **kwargs)

    def _readJSON(self, file, **kwargs):
        return self._dataForModel("readJSON", file=file, **kwargs)

    def _readCSV(self, file, **kwargs):
        return self._dataForModel("readCSV", file=file, **kwargs)

    def _createDir(self, directory):
        self._modelUpdated("createDir", directory=directory)

    def _deleteDir(self, directory):
        self._modelUpdated("deleteDir", directory=directory)

    def _copyFile(self, source, destination):
        self._modelUpdated("copyFile", source=source, destination=destination)

    def _deleteFile(self, file):
        self._modelUpdated("deleteFile", file=file)

    def _writeFile(self, data, file, **kwargs):
        self._modelUpdated("writeFile", data=data, file=file, **kwargs)

    def _writeJSON(self, obj, file, **kwargs):
        self._modelUpdated("writeJSON", obj=obj, file=file, **kwargs)

    def _writeCSV(self, data, file, **kwargs):
        self._modelUpdated("writeCSV", data=data, file=file, **kwargs)

    def _shellCmd(self, command, **kwargs):
        return self._modelUpdated("shellCmd", command=command, **kwargs)

    # Methods to be overridden by subclasses:

    # This method should return a model value for the given key to the
    # controller.
    def value(self, key, **kwargs):
        return None

    # This method should update the model when notified by the controller to
    # do so, and return a result.
    def update(self, key, **kwargs):
        return None
