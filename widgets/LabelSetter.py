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

# LabelSetter widget
# A bundling of three Labels followed by a Button. When the button is invoked,
# a dialog appears to allow the user to set the new value of the middle label.
# The widget can specify integer, float, or string values, with minimum and
# maximum values for numbers.
# New options:
# buttonText, buttonOptions, dialogTitle, dialogPrompt, labelType,
# labelOptions, minvalue, maxvalue, postOptions, postText, preOptions, preText
# TODO: better value handling of all the widgets

import tkinter as tk
import tkinter.simpledialog as sd
from ..core import constants as mtk
from .base.Frame import Frame
from .base.Label import Label
from .base.DoubleVar import DoubleVar
from .base.IntVar import IntVar
from .base.StringVar import StringVar
from .base.Button import Button

defaultOptions = {
    "buttonText": "Change",
    "labelText": "",
    "dialogTitle": "Enter Value",
    "dialogPrompt": "Enter the new value:",
}

packOptions = {
    "packAnchor": tk.W,
    "packSide": tk.LEFT,
}

dialogKeys = {
    "minvalue": None,
    "maxvalue": None,
    "dialogTitle": "title",
    "dialogPrompt": "prompt",
}


class LabelSetter(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.addDefaultOptions(defaultOptions)
        self.preLabel = self._getWidget("pre", Label)
        match self.option("labelType"):
            case "integer":
                self._labelVar = IntVar(self)
                self.dialog = tk.simpledialog.askinteger
                self._noneValue = 0
            case "float":
                self._labelVar = DoubleVar(self)
                self.dialog = tk.simpledialog.askfloat
                self._noneValue = 0.0
            case _:
                self._labelVar = StringVar(self)
                self.dialog = tk.simpledialog.askstring
                self._noneValue = ""
        self.label = self._getWidget("label", Label, self._labelVar)
        self.postLabel = self._getWidget("post", Label)
        self.button = self._getWidget("button", Button)
        self.button.pack(padx=5)
        self.button.registerObserver(self)
        self.dialogOptions = self.optionSet(dialogKeys)

    def value(self, key=None):
        return self._labelVar.get()

    def setValue(self, value, key=None):
        if value is None:
            value = self._noneValue
        self._labelVar.set(value)

    def setState(self, state, key=None):
        if self.preLabel:
            self.preLabel.setState(state)
        self.label.setState(state)
        if self.postLabel:
            self.postLabel.setState(state)
        self.button.setState(state)

    def reset(self):
        self.setValue(self._valueFromController())

    def widgetUpdated(self, widget, event=None, key=None, **kwargs):
        newValue = self.dialog(parent=self.winfo_toplevel(),
                               **self.dialogOptions)
        if newValue is not None:
            self.setValue(newValue)
            self._notifyObservers(self, mtk.VALUE_CHANGED)

    # Create a widget of the given class with either a dictionary of options
    # from the option key "<optionName>Options", or with just the text option
    # from the option key "<optionName>Text". If neither option exists, return
    # None. If a variable var is provided, add it as a textvariable option to
    # the new object.
    def _getWidget(self, optionName, cls, var=None):
        options = self.optionSet({optionName + "Text": "text"})
        options = self.option(optionName + "Options", options)
        if var:
            options["textvariable"] = var
        if options:
            return cls(self, **(options | packOptions))
        return None

    def destroy(self) -> None:
        self.button.unregisterObserver(self)
        super().destroy()
