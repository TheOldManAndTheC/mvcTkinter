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

# FileSelector widget
# A bundling of a Label, Entry and Button to implement a simple validating
# file selector.
# New options:
# buttonText, dirDialog, fileDialog, fileTypes, labelText

import os
import tkinter as tk
from tkinter import filedialog as fd
from .base.Frame import Frame
from .base.Label import Label
from .base.Entry import Entry
from .base.Button import Button

defaultOptions = {
    "fileDialog": "Choose File",
    "dirDialog": "Choose Directory"
}

packTop = {"packAnchor": tk.NW, "packSide": tk.TOP}
packLeft = {"packSide": tk.LEFT}
fillX = {"packFill": tk.X}
fillNone = {"packFill": tk.NONE}
expand = {"packExpand": True}


class FileSelector(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.addDefaultOptions(defaultOptions)
        self.fileTypes = self.option("fileTypes", [])
        self.label = Label(self, text=self.option("labelText", ""),
                           **(packTop | fillNone))
        entryFrame = Frame(self, **(packTop | fillX))
        self.entry = Entry(entryFrame, **(packLeft | fillX | expand))
        self.entry.registerObserver(self)
        self._binding = self.entry.bind("<FocusOut>",
                                        lambda *_: self.focusOut())
        self.button = Button(entryFrame, text=self.option("buttonText", ""),
                             command=self.buttonPressed, packPadx=10,
                             **packLeft)

    def value(self, key=None):
        match key:
            case "lastDirectory":
                return os.path.dirname(self.entry.value())
        return self.entry.value()

    def setValue(self, value, key=None):
        self.entry.setValue(value)

    def setState(self, state, key=None):
        self.label.setState(state, key)
        self.entry.setState(state, key)
        self.button.setState(state, key)

    def reset(self):
        self.setValue(self._valueFromController())

    def buttonPressed(self):
        initialDir = os.getcwd()
        value = self._valueFromController()
        if value is not None and os.path.exists(value):
            initialDir = os.path.dirname(value)
        if self.fileTypes:
            path = fd.askopenfilename(parent=self, initialdir=initialDir,
                                      title=self.option("fileDialog"),
                                      filetypes=self.fileTypes)
        else:
            path = fd.askdirectory(parent=self, initialdir=initialDir,
                                   title=self.option("dirDialog"),
                                   mustexist=True)
        if path:
            self.entry.setValue(path)

    # when the entry text changes, make sure it's a valid path before notifying
    def widgetUpdated(self, widget, event=None, key=None, **kwargs):
        if not os.path.exists(self.entry.value()):
            self.entry.config(foreground="red")
            return
        if self.fileTypes:
            found = False
            for (_, fileType) in self.fileTypes:
                if self.entry.value().endswith(fileType):
                    found = True
                    break
            if not found:
                self.entry.config(foreground="red")
                return
        self._notifyObservers(self)
        self.entry.config(foreground="black")

    # TODO: look into using validatecommand?
    # when the entry loses focus, if the value in it does not match the
    # validated path from the controller, restore it
    def focusOut(self):
        value = self._valueFromController()
        if value is not None and self.entry.value() != value:
            self.entry.setValue(value)

    def destroy(self) -> None:
        self.entry.unregisterObserver(self)
        self.entry.unbind("<FocusOut>", self._binding)
        super().destroy()
