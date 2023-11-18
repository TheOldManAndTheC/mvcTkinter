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

# Controller superclass
# Provides connections to a model object and a view object with widget
# management, and a facility for accessing application settings
# Options:
# model, name, view
from warnings import warn
from .core.OptionsMixin import OptionsMixin
from .core import fileIO


class Controller(OptionsMixin):
    def __init__(self, **options):
        self.options = options
        self._name = self.option("name")
        self._model = None
        self._view = None
        self._viewActive = False
        self.widgets = dict()
        self.setModel(self.option("model"))
        self.setView(self.option("view"))

    # This method returns the name of the controller. Provided only to keep
    # in line with the rest of the MVC spec.
    def name(self):
        return self._name

    # This model returns the model object for the controller
    def model(self):
        return self._model

    # This method sets the model object for the controller.
    def setModel(self, model):
        if self.model() == model:
            return
        if self.model() is not None:
            self.model().setController(None)
        if model:
            self._model = model
            model.setController(self)

    # This method returns the view object for the controller
    def view(self):
        return self._view

    # This method sets the view object for the controller.
    def setView(self, view):
        if self.view() == view:
            return
        if self.view() is not None:
            self.view().setController(None)
        if view:
            self._view = view
            view.setController(self)

    # This method registers a widget to the controller. Note that widgets that
    # are to be registered should have unique names.
    def registerWidget(self, widget):
        if widget.name() in self.widgets:
            warn("Previously registered widget: " + widget.name(),
                 RuntimeWarning)
        self.widgets[widget.name()] = widget

    # This method unregisters a widget from the controller.
    def unregisterWidget(self, widget):
        if widget.name() in self.widgets:
            self.widgets.pop(widget.name())

    # Methods to be overridden by subclasses:

    # This method should be used to handle any setup that should only occur
    # after the view has been fully created. It should be called by the view
    # once setup is complete.
    def _viewActivated(self):
        self._viewActive = True

    # This method should be used to get the value of an application setting for
    # the given setting key
    def settingValue(self, setting):
        return fileIO.settingValue(setting)

    # This method should be used to set the value of an application setting for
    # the given setting key.
    def setSetting(self, setting, value, write=True):
        fileIO.setSetting(setting, value, write)

    # This method should be called by the model to obtain external data from
    # the controller associated with the given key.
    def dataForModel(self, key, **kwargs):
        match key:
            case "currentDir":
                return fileIO.currentDir()
            case "pathExists":
                return fileIO.pathExists(**kwargs)
            case "latestFile":
                return fileIO.latestFile(**kwargs)
            case "readFile":
                return fileIO.readFile(**kwargs)
            case "readJSON":
                return fileIO.readJSON(**kwargs)
            case "readCSV":
                return fileIO.readCSV(**kwargs)
        return None

    # This method should be called by the model when something internal to the
    # model has changed that the controller needs to be notified about.
    def modelUpdated(self, key, **kwargs):
        match key:
            case "createDir":
                fileIO.createDirectory(**kwargs)
            case "deleteDir":
                fileIO.deleteDirectory(**kwargs)
            case "copyFile":
                fileIO.copyFile(**kwargs)
            case "deleteFile":
                fileIO.deleteFile(**kwargs)
            case "writeFile":
                fileIO.writeFile(**kwargs)
            case "writeJSON":
                fileIO.writeJSON(**kwargs)
            case "writeCSV":
                fileIO.writeCSV(**kwargs)
            case "shellCmd":
                return fileIO.shellCmd(**kwargs)

    # This method should be called by the model when the user should be
    # notified about something related to the model that isn't necessarily
    # a model update.
    def output(self, key=None, *args):
        return

    # This method should be called by widgets to obtain the correct model
    # values that the widget should display.
    def valueForWidget(self, widget, key=None, **kwargs):
        return None

    # This method should be called by widgets when user interaction occurs.
    def widgetUpdated(self, widget, event=None, key=None, **kwargs):
        return
