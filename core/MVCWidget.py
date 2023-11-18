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

# An MVC friendly wrapper for generic tkinter widgets
# Provides some basic integration with a controller object and option handling,
# as well as tags, observer object registration and notification, child
# widget generation and management, and self packing.
# Options:
# controller, name, parent, subWidgets, tags, tooltip
# Note: Tkinter base subclasses should multiple inherit with
# (MVCWidget, <class>)

import importlib
from .OptionsMixin import OptionsMixin
from .Tooltip import Tooltip

tkPackOptions = {
    "packAfter": "after",
    "packAnchor": "anchor",
    "packBefore": "before",
    "packExpand": "expand",
    "packFill": "fill",
    "packIn": "in",
    "packIpadx": "ipadx",
    "packIpady": "ipady",
    "packPadx": "padx",
    "packPady": "pady",
    "packSide": "side",
}


class MVCWidget(OptionsMixin):
    def __init__(self, parent=None, **options):
        self.parent = parent
        self.options = options
        self._registered = False
        self._controller = None
        self._observers = []
        self._observing = []
        self.setController(self.option("controller"))
        if hasattr(self.parent, "widgets") and \
                self.name() not in self.parent.widgets:
            self.parent.widgets[self.name()] = self
        self.tags = self.option("tags", [])
        self.widgets = dict()
        self._parseSubWidgets()
        if hasattr(self, "config"):
            self.config(**self.optionsForTkWidget(self))
        if hasattr(self, "pack"):
            packOptions = self.optionsForTkWidget()
            # only pack if pack options were passed
            if packOptions:
                self.pack(**packOptions)
        self._tooltip = None
        if self.option("tooltip"):
            self._tooltip = Tooltip(self, text=self.option("tooltip"))

    # This method returns the name of the widget. If a name was not specified
    # in the options, the default Tkinter widget name is returned.
    def name(self):
        return self.option("name", self._name)

    # This method returns the full unique key path for the widget.
    def keyPath(self):
        path = self.name()
        if self.parent is not None and hasattr(self.parent, "keyPath"):
            path = self.parent.keyPath() + "." + path
        return path

    # This method returns the controller object for this widget.
    def controller(self):
        return self._controller

    # This method sets the controller object for this widget. If the widget
    # is already registered with a controller, it will be unregistered from
    # that controller and registered to the new one. Note that if the widget is
    # not named, it can't be registered.
    def setController(self, controller):
        if self.controller() == controller:
            return
        if self._registered:
            self._unregisterController()
        self._controller = controller
        self._registerController()

    # This method registers the widget with the controller object, so the
    # controller can access the widget.
    def _registerController(self):
        if self._registered or self._controller is None:
            return
        self._controller.registerWidget(self)
        self._registered = True

    # This method unregisters the widget from the controller object.
    def _unregisterController(self):
        if not self._registered:
            return
        self._controller.unregisterWidget(self)
        self._registered = False

    # This method returns the controller's value for the given key for this
    # widget, or None if no controller is registgered.
    def _valueFromController(self, key=None, **kwargs):
        if self._registered:
            return self._controller.valueForWidget(self, key, **kwargs)
        return None

    # This method should be called by objects who want to be notified of
    # widget events that the controller object gets.
    def registerObserver(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    # This method should be called by observing objects who want to stop being
    # notified of widget events.
    def unregisterObserver(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    # This method should be called by any subclass methods that update the
    # controller object
    def _notifyObservers(self, widget, event=None, key=None, **kwargs):
        if self._controller and self._registered:
            self._controller.widgetUpdated(widget, event, key, **kwargs)
        for observer in self._observers:
            observer.widgetUpdated(widget, event, key, **kwargs)

    # This method will return all the options in self.options that apply to the
    # passed Tkinter widget. By default, it returns all the options that are
    # valid pack options.
    def optionsForTkWidget(self, tkWidget=None):
        if tkWidget is None:
            keys = tkPackOptions
        else:
            keys = list(tkWidget.config().keys())
        return self.optionSet(keys)

    # This method returns the sub-widget at the given partial key path,
    # separated by '.'. If the path does not reach a widget, returns None.
    def getSubWidget(self, keyPath):
        keys = keyPath.split(".")
        widget = None
        widgets = self.widgets
        for key in keys:
            if key not in widgets:
                return None
            widget = widgets[key]
            widgets = widget.widgets
        return widget

    # This method constructs child widgets based on data from an optional
    # "subWidgets" key in the options.
    # The subWidgets should be an array containing one or more dictionaries,
    # each holding a set of widget options that must include a "className"
    # key with a string value that is the name of a widget class from this
    # package.
    # If there is a "name" key in the widget options, the child widget will
    # be added to the self.widgets dictionary under that name.
    # Subwidget options can also have a "subWidgets" entry, allowing for
    # recursive construction of more complex widget arrangements.
    def _parseSubWidgets(self):
        for widgetDict in self.option("subWidgets", []):
            widgetPackages = ["..widgets.", "..widgets.base.", ".."]
            for package in widgetPackages:
                try:
                    module = importlib.import_module(package +
                                                     widgetDict["className"],
                                                     __package__)
                except ModuleNotFoundError:
                    continue
                break
            cls = getattr(module, widgetDict["className"])
            widget = cls(self, **widgetDict)
            self.widgets[widget.name()] = widget

    # Methods to be overridden by subclasses:

    # This method should be used to return any values displayed in the widget.
    def value(self, key=None):
        return None

    # This method should be used to set values displayed in the widget.
    def setValue(self, value, key=None):
        return

    # This method should be used to set the Tkinter state for the widget.
    def setState(self, state, key=None):
        return

    # This method should be used to redraw the contents of the widget.
    def refresh(self):
        return

    # This method should re-query the controller for all the data this widget
    # displays. By default, it sets the widget's value to one provided by the
    # controller.
    def reset(self):
        self.setValue(self._valueFromController())

    # This method should handle any widget notifications from widgets being
    # observed by this widget. By default, it in turn sends a notification
    # to its observers that it has updated.
    def widgetUpdated(self, widget, event=None, key=None, **kwargs):
        self._notifyObservers(self, event, key, **kwargs)
