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

# LabeledEntry widget
# A simple bundling of an Entry with a Label on either side.
# Options:
# entryOptions, postOptions, postText, preOptions, preText
# TODO: better value handling of both label and entry

import tkinter as tk
from .base.Frame import Frame
from .base.Label import Label
from .base.Entry import Entry

packOptions = {"packAnchor": tk.W, "packSide": tk.LEFT}


class LabeledEntry(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.preLabel = self._getWidget("pre", Label)
        self.entry = Entry(self, packPadx=5,
                           **(self.option("entryOptions", dict()) |
                              packOptions))
        self.postLabel = self._getWidget("post", Label)
        self.entry.registerObserver(self)

    def value(self, key=None):
        return self.entry.value()

    def setValue(self, value, key=None):
        self.entry.setValue(value)

    def setState(self, state, key=None):
        if self.preLabel:
            self.preLabel.setState(state, key)
        self.entry.setState(state, key)
        if self.postLabel:
            self.postLabel.setState(state, key)

    def reset(self):
        self.entry.setValue(self._valueFromController())

    # Create a widget of the given class with either a dictionary of options
    # from the option key "<optionName>Options", or with just the text option
    # from the option key "<optionName>Text". If neither option exists, return
    # None.
    def _getWidget(self, optionName, cls):
        options = self.optionSet({optionName + "Text": "text"})
        options = self.option(optionName + "Options", options)
        if options:
            return cls(self, **(options | packOptions))
        return None

    def destroy(self) -> None:
        self.entry.unregisterObserver(self)
        super().destroy()
