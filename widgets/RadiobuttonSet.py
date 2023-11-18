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

# RadiobuttonSet widget
# A grouping of Radiobuttons that use a common variable with an optional
# Label header.
# New options:
# buttons, labelOptions, labelText, variable
# TODO: test

import tkinter as tk
from ..core import constants as mtk
from ..core.MVCWidget import MVCWidget
from .base.Frame import Frame
from .base.Label import Label
from .base.StringVar import StringVar
from .base.Radiobutton import Radiobutton

packOptions = {"packAnchor": tk.NW, "packSide": tk.TOP, "packFill": tk.NONE}


class RadiobuttonSet(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.radiobuttons = []
        self.label = None
        labelOptions = self.option("labelOptions",
                                   {"text": self.option("labelText")})
        if labelOptions:
            self.label = Label(self, **(labelOptions | packOptions))
        self._trace = None
        self._variable = None
        self.setValue(self.option("variable",
                                  StringVar(self, name=self.option("varName"))),
                      "variable")
        buttons = self.option("buttons")
        buttonTooltips = False
        for buttonOptions in buttons:
            self.radiobuttons.append(
                Radiobutton(self, variable=self.value("variable"),
                            **(buttonOptions | packOptions))
            )
            if "tooltip" in buttonOptions:
                buttonTooltips = True
        # only have the main tooltip cover the whole area if the individual
        # buttons don't have tooltips
        if self._tooltip is not None and buttonTooltips:
            # apply the tooltip only to the header label
            self._tooltip.bindTooltip(self.label)
            # let the label extend the length of the frame
            self.label.pack(fill=tk.X)

    def value(self, key=None):
        match key:
            case "variable":
                return self._variable
        return self._variable.get()

    def setValue(self, value, key=None):
        match key:
            case "variable":
                if self._variable != value:
                    self._unregisterVariable()
                    self._variable = value
                    for radiobutton in self.radiobuttons:
                        radiobutton.config(variable=self._variable)
                    self._registerVariable()
                return
        self._variable.set(value)

    def _registerVariable(self):
        if self._variable is None:
            return
        if issubclass(self._variable, MVCWidget):
            self._variable.registerObserver(self)
        else:
            self._trace = self._variable.trace_add(
                "write",
                lambda *_: self._notifyObservers(self, mtk.VALUE_CHANGED))

    def _unregisterVariable(self):
        if self._trace is not None:
            self._variable.trace_remove("write", self._trace)
            self._trace = None
        elif self._variable is not None:
            self._variable.unregisterObserver(self)

    def destroy(self) -> None:
        self._unregisterVariable()
        super().destroy()
